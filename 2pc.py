from manim import (
    Scene,
    Square,
    Circle,
    TAU,
    PINK,
    BLUE,
    WHITE,
    Create,
    Transform,
    FadeOut,
    Text,
    MathTex,
    VGroup,
    Arrow,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    Write,
    Table,
    GREEN,
    RED,
    Polygon,
    Line,
    config,
    ReplacementTransform,
    Indicate,
    Wait,
)


class XORGateAnimation(Scene):
    def construct(self):
        # Title
        title = Text("XOR Gate Logic", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Create XOR symbol
        xor_gate = self.create_xor_gate()
        xor_gate.scale(0.8)
        xor_gate.to_edge(LEFT)
        xor_gate.shift(UP * 0.5)
        
        # XOR explanation
        xor_text = Text("XOR (Exclusive OR)", font_size=30)
        xor_text.next_to(title, DOWN)
        
        explanation = Text(
            "Output is TRUE if inputs are different", 
            font_size=24
        )
        explanation.next_to(xor_text, DOWN)
        
        self.play(Write(xor_text))
        self.play(Write(explanation))
        self.play(Create(xor_gate))
        self.wait(1)

        # Create truth table
        truth_table = self.create_truth_table()
        truth_table.scale(0.8)
        truth_table.to_edge(RIGHT)
        
        self.play(Create(truth_table))
        self.wait(1)

        # Animate each row of the truth table
        self.animate_truth_table_rows(xor_gate, truth_table)
        
        # Final message
        final_text = Text("XOR is fundamental in cryptography and error detection", font_size=24)
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

    def create_xor_gate(self):
        # Create XOR gate symbol
        gate_body = Polygon(
            [-1, 1, 0], 
            [1, 0, 0], 
            [-1, -1, 0], 
            color=WHITE
        )
        
        # Add the curved input side
        curve = Arc(
            start_angle=-PI/2,
            angle=PI,
            radius=0.25,
            arc_center=[-1.25, 0, 0],
            color=WHITE
        )
        
        # Input and output lines
        input_line1 = Line([-2, 0.5, 0], [-1, 0.5, 0], color=WHITE)
        input_line2 = Line([-2, -0.5, 0], [-1, -0.5, 0], color=WHITE)
        output_line = Line([1, 0, 0], [2, 0, 0], color=WHITE)
        
        # Input and output labels
        input_a = Text("A", font_size=24).next_to(input_line1, LEFT)
        input_b = Text("B", font_size=24).next_to(input_line2, LEFT)
        output = Text("Output", font_size=24).next_to(output_line, RIGHT)
        
        return VGroup(
            gate_body, curve, input_line1, input_line2, output_line,
            input_a, input_b, output
        )

    def create_truth_table(self):
        table = Table(
            [["A", "B", "A ⊕ B"],
             ["0", "0", "0"],
             ["0", "1", "1"],
             ["1", "0", "1"],
             ["1", "1", "0"]],
            row_labels=[Text(""), Text("Case 1"), Text("Case 2"), Text("Case 3"), Text("Case 4")],
            include_outer_lines=True
        )
        
        # Color the output column
        table.add_highlighted_cell((2, 3), color=RED)
        table.add_highlighted_cell((3, 3), color=GREEN)
        table.add_highlighted_cell((4, 3), color=GREEN)
        table.add_highlighted_cell((5, 3), color=RED)
        
        return table

    def animate_truth_table_rows(self, xor_gate, truth_table):
        # Case 1: A=0, B=0
        self.highlight_row_and_show_signals(xor_gate, truth_table, row=2, a_value=0, b_value=0, output_value=0)
        
        # Case 2: A=0, B=1
        self.highlight_row_and_show_signals(xor_gate, truth_table, row=3, a_value=0, b_value=1, output_value=1)
        
        # Case 3: A=1, B=0
        self.highlight_row_and_show_signals(xor_gate, truth_table, row=4, a_value=1, b_value=0, output_value=1)
        
        # Case 4: A=1, B=1
        self.highlight_row_and_show_signals(xor_gate, truth_table, row=5, a_value=1, b_value=1, output_value=0)

    def highlight_row_and_show_signals(self, xor_gate, truth_table, row, a_value, b_value, output_value):
        # Highlight the current row
        row_highlight = truth_table.get_highlighted_cell(
            (row, 1), color=BLUE, opacity=0.3
        )
        row_highlight.stretch_to_fit_width(truth_table.get_width())
        row_highlight.move_to(truth_table.get_cell((row, 2)))
        
        # Create signal indicators
        a_signal = Circle(radius=0.2, color=GREEN if a_value else RED, fill_opacity=0.8)
        a_signal.move_to(xor_gate[2].get_start())  # Position at input A
        
        b_signal = Circle(radius=0.2, color=GREEN if b_value else RED, fill_opacity=0.8)
        b_signal.move_to(xor_gate[3].get_start())  # Position at input B
        
        output_signal = Circle(radius=0.2, color=GREEN if output_value else RED, fill_opacity=0.8)
        output_signal.move_to(xor_gate[4].get_end())  # Position at output
        
        # Show the row and signals
        self.play(Create(row_highlight))
        self.play(Create(a_signal), Create(b_signal))
        
        # Animate signals flowing through the gate
        a_signal_copy = a_signal.copy()
        b_signal_copy = b_signal.copy()
        
        self.play(
            a_signal_copy.animate.move_to(xor_gate[0].get_center()),
            b_signal_copy.animate.move_to(xor_gate[0].get_center()),
        )
        
        self.play(
            ReplacementTransform(
                VGroup(a_signal_copy, b_signal_copy), 
                output_signal
            )
        )
        
        # Highlight the result in the truth table
        result_cell = truth_table.get_entries((row, 3))
        self.play(Indicate(result_cell))
        
        self.wait(1)
        
        # Clean up for next case
        self.play(
            FadeOut(row_highlight),
            FadeOut(a_signal),
            FadeOut(b_signal),
            FadeOut(output_signal)
        )


if __name__ == "__main__":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_rate = 30
    scene = XORGateAnimation()
    scene.render()
