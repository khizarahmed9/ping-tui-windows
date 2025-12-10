import subprocess
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Input, Checkbox, Button, Label, Static, RichLog, ContentSwitcher

class PingTUIWindows(App):
    CSS = """
    Screen { layout: vertical; }

    #config-view {
        padding: 0 1;
        overflow-y: auto; 
    }

    #top-section {
        height: auto;
        margin-bottom: 0; 
        border: solid $accent;
        background: $surface;
        padding: 0 1;
    }

    #mid-section {
        height: auto;
        layout: horizontal; 
        margin-top: 0;
    }

    .column-box {
        width: 1fr;
        height: auto;
        border: solid $accent;
        background: $surface;
        margin-right: 1;
        padding: 0 1;
    }
    .column-box:last-of-type { margin-right: 0; }

    .section-title {
        background: $surface;
        color: $accent-lighten-2;
        padding: 0 1;
        offset-y: -1;
        text-style: bold;
        dock: top;
        width: auto;
    }

    .item-container {
        margin-bottom: 0; 
        padding-bottom: 1;
    }

    .help-text {
        color: $text-muted;
        text-style: italic;
        margin-left: 2;
        height: auto; 
    }

    .input-row {
        height: 1;
        align: left middle;
    }

    Label.lbl {
        color: $text-muted;
        width: 14; 
    }

    .input-val {
        height: 1;
        border: none;
        background: $surface-darken-1;
        width: 1fr;
    }
    .input-val:focus { background: $accent-darken-2; }

    #footer-container {
        dock: bottom;
        height: auto;
        background: $surface-darken-1;
        border-top: solid $primary;
        padding: 0 1;
    }

    .cmd-preview {
        background: $surface;
        color: $secondary-lighten-2;
        padding: 0 1;
        margin-bottom: 0;
        height: auto;
    }

    #btn-run { width: 100%; margin-top: 1; }
    #log-view { display: none; height: 1fr; }
    """

    BINDINGS = [("escape", "toggle_view", "Back")]

    def _build_checkbox_row(self, widget, help_str):
        return Vertical(
            widget,
            Label(help_str, classes="help-text"),
            classes="item-container"
        )

    def _build_input_row(self, label_text, id, placeholder, help_str):
        return Vertical(
            Horizontal(
                Label(label_text, classes="lbl"),
                Input(placeholder=placeholder, id=id, classes="input-val"),
                classes="input-row"
            ),
            Label(help_str, classes="help-text"),
            classes="item-container"
        )

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with ContentSwitcher(initial="config-view", id="switcher"):
            with Vertical(id="config-view"):
                # Target Section
                with Container(id="top-section"):
                    yield Label(" Target ", classes="section-title")
                    yield Input(placeholder="e.g. google.com", id="target")
                    yield Label("The website address or IP you want to check connection to.", classes="help-text")

                # Options Grid
                with Horizontal(id="mid-section"):
                    with Container(classes="column-box"):
                        yield Label(" Options ", classes="section-title")
                        yield self._build_checkbox_row(Checkbox("Infinite (-t)", id="flag_t"), "Run until stopped.")
                        yield self._build_checkbox_row(Checkbox("Resolve (-a)", id="flag_a"), "Show hostnames.")
                        yield self._build_checkbox_row(Checkbox("No Frag (-f)", id="flag_f"), "Don't split packets.")
                        yield self._build_checkbox_row(Checkbox("IPv4 Only (-4)", id="flag_4"), "Force IPv4.")
                        yield self._build_checkbox_row(Checkbox("IPv6 Only (-6)", id="flag_6"), "Force IPv6.")
                        yield self._build_checkbox_row(Checkbox("Hyper-V (-p)", id="flag_p"), "Test VM connection.")

                    with Container(classes="column-box"):
                        yield Label(" Basics ", classes="section-title")
                        yield self._build_input_row("Count (-n)", "val_n", "4", "Total pings.")
                        yield self._build_input_row("Size (-l)", "val_l", "32", "Packet size.")
                        yield self._build_input_row("Timeout (-w)", "val_w", "ms", "Max wait time.")
                        yield self._build_input_row("TTL (-i)", "val_i", "Def", "Max hops.")

                    with Container(classes="column-box"):
                        yield Label(" Advanced ", classes="section-title")
                        yield self._build_input_row("Source (-S)", "val_S", "IP", "Local IP.")
                        yield self._build_input_row("TOS (-v)", "val_v", "0", "Priority.")
                        yield self._build_input_row("Route (-r)", "val_r", "#", "Count hops.")
                        yield self._build_input_row("Comp (-c)", "val_c", "ID", "Compartment ID.")

                # Footer
                with Container(id="footer-container"):
                    yield Label("Command Preview:", classes="help-text")
                    yield Static("ping [target]", id="cmd_text", classes="cmd-preview")
                    yield Button("EXECUTE PING", variant="success", id="btn-run")

            with Vertical(id="log-view"):
                yield RichLog(id="output_log", markup=True, highlight=True)

        yield Footer()

    # Scrolling fix
    def on_descendant_focus(self, event):
        event.widget.scroll_visible(animate=False)

    def on_input_changed(self, event):
        self.update_preview()

    def on_checkbox_changed(self, event):
        self.update_preview()

    def update_preview(self):
        cmd = ["ping"]

        # Boolean flags
        flags = [
            ("#flag_t", "-t"), ("#flag_a", "-a"), ("#flag_f", "-f"),
            ("#flag_4", "-4"), ("#flag_6", "-6"), ("#flag_p", "-p")
        ]
        for ui_id, flag in flags:
            if self.query_one(ui_id).value:
                cmd.append(flag)

        # Value flags
        value_flags = [
            ("val_n", "-n"), ("val_l", "-l"), ("val_w", "-w"), ("val_i", "-i"),
            ("val_S", "-S"), ("val_v", "-v"), ("val_r", "-r"), ("val_c", "-c")
        ]

        for ui_id, flag in value_flags:
            val = self.query_one(f"#{ui_id}").value.strip()
            if val:
                cmd.extend([flag, val])

        target = self.query_one("#target").value.strip()
        cmd.append(target if target else "[target]")

        self.current_command = cmd
        self.query_one("#cmd_text").update(" ".join(cmd))

    def on_button_pressed(self, event):
        if event.button.id != "btn-run":
            return

        if not self.query_one("#target").value:
            self.notify("Target required!", severity="error")
            return

        self.query_one("#switcher").current = "log-view"
        log = self.query_one("#output_log")
        log.clear()
        log.write(f"[bold green]Running: {' '.join(self.current_command)}[/]")
        self.run_process(self.current_command)

    def action_toggle_view(self):
        switcher = self.query_one("#switcher")
        if switcher.current == "log-view":
            switcher.current = "config-view"
        else:
            self.exit()

    @work(exclusive=True, thread=True)
    def run_process(self, cmd_list):
        log = self.query_one("#output_log")
        try:
            with subprocess.Popen(
                    cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            ) as proc:
                for line in proc.stdout:
                    self.call_from_thread(log.write, line.strip())

            self.call_from_thread(log.write, "[red]-- Stopped --[/]")
        except Exception as e:
            self.call_from_thread(log.write, f"[red]Error: {e}[/]")


if __name__ == "__main__":
    PingTUIWindows().run()