from manim import (
    Scene,
    Square,
    Circle,
    Arc,
    PI,
    TAU,
    PINK,
    BLUE,
    WHITE,
    YELLOW,
    PURPLE,
    ORANGE,
    Create,
    Transform,
    FadeOut,
    FadeIn,
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
    Rectangle,
    DashedLine,
    CurvedArrow,
    LabeledDot,
    Tex,
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

        explanation = Text("Output is TRUE if inputs are different", font_size=24)
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
        final_text = Text(
            "XOR is fundamental in cryptography and error detection", font_size=24
        )
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

    def create_xor_gate(self):
        # Create XOR gate symbol
        gate_body = Polygon([-1, 1, 0], [1, 0, 0], [-1, -1, 0], color=WHITE)

        # Add the curved input side
        curve = Arc(
            start_angle=-PI / 2,
            angle=PI,
            radius=0.25,
            arc_center=[-1.25, 0, 0],
            color=WHITE,
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
            gate_body,
            curve,
            input_line1,
            input_line2,
            output_line,
            input_a,
            input_b,
            output,
        )

    def create_truth_table(self):
        table = Table(
            [
                ["A", "B", "A ⊕ B"],
                ["0", "0", "0"],
                ["0", "1", "1"],
                ["1", "0", "1"],
                ["1", "1", "0"],
            ],
            row_labels=[
                Text(""),
                Text("Case 1"),
                Text("Case 2"),
                Text("Case 3"),
                Text("Case 4"),
            ],
            include_outer_lines=True,
        )

        # Color the output column
        table.add_highlighted_cell((2, 3), color=RED)
        table.add_highlighted_cell((3, 3), color=GREEN)
        table.add_highlighted_cell((4, 3), color=GREEN)
        table.add_highlighted_cell((5, 3), color=RED)

        return table

    def animate_truth_table_rows(self, xor_gate, truth_table):
        # Case 1: A=0, B=0
        self.highlight_row_and_show_signals(
            xor_gate, truth_table, row=2, a_value=0, b_value=0, output_value=0
        )

        # Case 2: A=0, B=1
        self.highlight_row_and_show_signals(
            xor_gate, truth_table, row=3, a_value=0, b_value=1, output_value=1
        )

        # Case 3: A=1, B=0
        self.highlight_row_and_show_signals(
            xor_gate, truth_table, row=4, a_value=1, b_value=0, output_value=1
        )

        # Case 4: A=1, B=1
        self.highlight_row_and_show_signals(
            xor_gate, truth_table, row=5, a_value=1, b_value=1, output_value=0
        )

    def highlight_row_and_show_signals(
        self, xor_gate, truth_table, row, a_value, b_value, output_value
    ):
        # Highlight the current row
        row_highlight = truth_table.get_highlighted_cell(
            (row, 1), color=BLUE, fill_opacity=0.3
        )
        row_highlight.stretch_to_fit_width(truth_table.get_width())
        row_highlight.move_to(truth_table.get_cell((row, 2)))

        # Create signal indicators
        a_signal = Circle(radius=0.2, color=GREEN if a_value else RED, fill_opacity=0.8)
        a_signal.move_to(xor_gate[2].get_start())  # Position at input A

        b_signal = Circle(radius=0.2, color=GREEN if b_value else RED, fill_opacity=0.8)
        b_signal.move_to(xor_gate[3].get_start())  # Position at input B

        output_signal = Circle(
            radius=0.2, color=GREEN if output_value else RED, fill_opacity=0.8
        )
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
            ReplacementTransform(VGroup(a_signal_copy, b_signal_copy), output_signal)
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
            FadeOut(output_signal),
        )


class ChainedGarbledGatesAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Chaining Garbled Gates in 2PC", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Introduction text
        intro_text = Text(
            "Secure computation using chained garbled circuits", font_size=24
        )
        intro_text.next_to(title, DOWN)
        self.play(Write(intro_text))
        self.wait(1)

        # Create the two parties
        alice = self.create_party("Alice (Garbler)", LEFT * 5 + UP * 2)
        bob = self.create_party("Bob (Evaluator)", RIGHT * 5 + UP * 2)
        
        self.play(Create(alice), Create(bob))
        self.wait(1)

        # Create the first garbled gate
        gate1 = self.create_garbled_gate("Gate 1 (AND)", LEFT * 2.5)
        self.play(Create(gate1))
        
        # Create the second garbled gate
        gate2 = self.create_garbled_gate("Gate 2 (XOR)", RIGHT * 2.5)
        self.play(Create(gate2))
        
        # Connect the gates with a wire
        connecting_wire = Arrow(
            gate1.get_right(), gate2.get_left(), 
            buff=0.1, color=YELLOW
        )
        self.play(Create(connecting_wire))
        
        # Label the wire
        wire_label = Text("Encrypted\nOutput Wire", font_size=16, color=YELLOW)
        wire_label.next_to(connecting_wire, UP, buff=0.1)
        self.play(Write(wire_label))
        self.wait(1)

        # Show inputs for the first gate
        input_a = Text("Input A", font_size=20, color=GREEN)
        input_a.next_to(gate1, UP + LEFT, buff=0.5)
        
        input_b = Text("Input B", font_size=20, color=BLUE)
        input_b.next_to(gate1, DOWN + LEFT, buff=0.5)
        
        input_a_wire = Arrow(input_a.get_right(), gate1.get_left() + UP * 0.5, buff=0.1, color=GREEN)
        input_b_wire = Arrow(input_b.get_right(), gate1.get_left() + DOWN * 0.5, buff=0.1, color=BLUE)
        
        self.play(
            Write(input_a), 
            Write(input_b),
            Create(input_a_wire),
            Create(input_b_wire)
        )
        self.wait(1)

        # Show input for the second gate
        input_c = Text("Input C", font_size=20, color=PURPLE)
        input_c.next_to(gate2, DOWN + LEFT, buff=0.5)
        
        input_c_wire = Arrow(input_c.get_right(), gate2.get_left() + DOWN * 0.5, buff=0.1, color=PURPLE)
        
        self.play(
            Write(input_c),
            Create(input_c_wire)
        )
        self.wait(1)

        # Show final output
        output = Text("Final Output", font_size=20, color=ORANGE)
        output.next_to(gate2, RIGHT, buff=0.5)
        
        output_wire = Arrow(gate2.get_right(), output.get_left(), buff=0.1, color=ORANGE)
        
        self.play(
            Write(output),
            Create(output_wire)
        )
        self.wait(1)

        # Animate the computation flow
        self.animate_computation_flow(
            gate1, gate2, connecting_wire, 
            input_a_wire, input_b_wire, input_c_wire, output_wire
        )
        
        # Show the garbling process
        self.explain_garbling(alice, bob, gate1, gate2)
        
        # Final explanation
        final_text = Text(
            "Chaining gates allows for complex secure computations", 
            font_size=24
        )
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)

    def create_party(self, name, position):
        party = VGroup()
        
        # Create person icon
        head = Circle(radius=0.3, color=WHITE)
        body = Rectangle(height=0.8, width=0.6, color=WHITE)
        body.next_to(head, DOWN, buff=0.1)
        
        person = VGroup(head, body)
        person.move_to(position)
        
        # Add name label
        label = Text(name, font_size=20)
        label.next_to(person, DOWN, buff=0.2)
        
        party.add(person, label)
        return party

    def create_garbled_gate(self, name, position):
        gate = VGroup()
        
        # Create gate box
        box = Rectangle(height=2, width=3, color=WHITE)
        box.set_fill(color=BLUE, opacity=0.2)
        
        # Add gate name
        label = Text(name, font_size=20)
        label.move_to(box.get_center())
        
        # Add input and output points
        input1 = Circle(radius=0.1, color=WHITE).move_to(box.get_left() + UP * 0.5)
        input2 = Circle(radius=0.1, color=WHITE).move_to(box.get_left() + DOWN * 0.5)
        output = Circle(radius=0.1, color=WHITE).move_to(box.get_right())
        
        # Add encryption indication
        lock_symbol = Text("🔒", font_size=24)
        lock_symbol.move_to(box.get_top() + DOWN * 0.4 + RIGHT * 1)
        
        gate.add(box, label, input1, input2, output, lock_symbol)
        gate.move_to(position)
        
        return gate

    def animate_computation_flow(self, gate1, gate2, connecting_wire, 
                                input_a_wire, input_b_wire, input_c_wire, output_wire):
        # Create signal dots
        signal_a = Circle(radius=0.15, color=GREEN, fill_opacity=0.8)
        signal_a.move_to(input_a_wire.get_start())
        
        signal_b = Circle(radius=0.15, color=BLUE, fill_opacity=0.8)
        signal_b.move_to(input_b_wire.get_start())
        
        # Animate inputs flowing into gate 1
        self.play(
            signal_a.animate.move_to(input_a_wire.get_end()),
            signal_b.animate.move_to(input_b_wire.get_end())
        )
        
        # Process in gate 1
        self.play(
            signal_a.animate.move_to(gate1.get_center()),
            signal_b.animate.move_to(gate1.get_center())
        )
        
        # Output from gate 1 becomes input to gate 2
        intermediate_signal = Circle(radius=0.15, color=YELLOW, fill_opacity=0.8)
        self.play(
            ReplacementTransform(
                VGroup(signal_a, signal_b), 
                intermediate_signal.move_to(connecting_wire.get_start())
            )
        )
        
        # Move intermediate signal along the wire
        self.play(intermediate_signal.animate.move_to(connecting_wire.get_end()))
        
        # Create signal for input C
        signal_c = Circle(radius=0.15, color=PURPLE, fill_opacity=0.8)
        signal_c.move_to(input_c_wire.get_start())
        
        # Animate input C flowing into gate 2
        self.play(signal_c.animate.move_to(input_c_wire.get_end()))
        
        # Process in gate 2
        self.play(
            intermediate_signal.animate.move_to(gate2.get_center()),
            signal_c.animate.move_to(gate2.get_center())
        )
        
        # Final output
        final_signal = Circle(radius=0.15, color=ORANGE, fill_opacity=0.8)
        self.play(
            ReplacementTransform(
                VGroup(intermediate_signal, signal_c), 
                final_signal.move_to(output_wire.get_start())
            )
        )
        
        # Move final signal to output
        self.play(final_signal.animate.move_to(output_wire.get_end()))
        self.wait(1)
        
        # Fade out the signal
        self.play(FadeOut(final_signal))

    def explain_garbling(self, alice, bob, gate1, gate2):
        # Clear some space
        explanation_area = Rectangle(
            width=10, height=3, 
            stroke_opacity=0, 
            fill_opacity=0
        )
        explanation_area.to_edge(DOWN, buff=1)
        
        # Step 1: Alice garbles the circuit
        step1 = Text("1. Alice garbles both gates with random labels", font_size=20)
        step1.move_to(explanation_area.get_top() + DOWN * 0.5)
        
        alice_arrow = CurvedArrow(
            alice.get_bottom() + DOWN * 0.2, 
            gate1.get_top() + UP * 0.2, 
            angle=-TAU/6,
            color=WHITE
        )
        
        self.play(Write(step1), Create(alice_arrow))
        self.wait(1)
        
        # Step 2: Alice sends garbled circuit to Bob
        step2 = Text("2. Alice sends garbled circuit and her encrypted inputs to Bob", font_size=20)
        step2.move_to(explanation_area.get_center())
        
        transfer_arrow = Arrow(
            alice.get_right(), 
            bob.get_left(), 
            buff=0.5,
            color=WHITE
        )
        
        self.play(Write(step2), Create(transfer_arrow))
        self.wait(1)
        
        # Step 3: Bob evaluates
        step3 = Text("3. Bob evaluates the circuit gate by gate", font_size=20)
        step3.move_to(explanation_area.get_bottom() + UP * 0.5)
        
        bob_arrow1 = CurvedArrow(
            bob.get_bottom() + DOWN * 0.2, 
            gate1.get_top() + RIGHT * 1 + UP * 0.2, 
            angle=TAU/6,
            color=WHITE
        )
        
        bob_arrow2 = CurvedArrow(
            bob.get_bottom() + DOWN * 0.2, 
            gate2.get_top() + UP * 0.2, 
            angle=TAU/6,
            color=WHITE
        )
        
        self.play(Write(step3), Create(bob_arrow1), Create(bob_arrow2))
        self.wait(1)
        
        # Cleanup
        self.play(
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(step3),
            FadeOut(alice_arrow),
            FadeOut(transfer_arrow),
            FadeOut(bob_arrow1),
            FadeOut(bob_arrow2)
        )


if __name__ == "__main__":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_rate = 30
    scene = ChainedGarbledGatesAnimation()
    scene.render()
