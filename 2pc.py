from manim import (
    # Scenes and configuration
    Scene,
    config,
    # Basic geometric shapes
    Arc,
    Circle,
    Dot,
    LabeledDot,
    Line,
    Polygon,
    Rectangle,
    Square,
    # Arrows and lines
    Arrow,
    CurvedArrow,
    DashedLine,
    # Text and math
    MathTex,
    Table,
    Tex,
    Text,
    # Groups and transformations
    SurroundingRectangle,
    Transform,
    VGroup,
    # Animation methods
    Create,
    Cross,
    FadeIn,
    FadeOut,
    FadeToColor,
    Indicate,
    ReplacementTransform,
    Wait,
    Write,
    # Colors
    BLUE,
    GREEN,
    ORANGE,
    PINK,
    PURPLE,
    RED,
    WHITE,
    YELLOW,
    YELLOW_C,
    # Constants and directions
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UP,
)
from manim_fontawesome import solid


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
            gate1.get_right(), gate2.get_left(), buff=0.1, color=YELLOW
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

        input_a_wire = Arrow(
            input_a.get_right(), gate1.get_left() + UP * 0.5, buff=0.1, color=GREEN
        )
        input_b_wire = Arrow(
            input_b.get_right(), gate1.get_left() + DOWN * 0.5, buff=0.1, color=BLUE
        )

        self.play(
            Write(input_a), Write(input_b), Create(input_a_wire), Create(input_b_wire)
        )
        self.wait(1)

        # Show input for the second gate
        input_c = Text("Input C", font_size=20, color=PURPLE)
        input_c.next_to(gate2, DOWN + LEFT, buff=0.5)

        input_c_wire = Arrow(
            input_c.get_right(), gate2.get_left() + DOWN * 0.5, buff=0.1, color=PURPLE
        )

        self.play(Write(input_c), Create(input_c_wire))
        self.wait(1)

        # Show final output
        output = Text("Final Output", font_size=20, color=ORANGE)
        output.next_to(gate2, RIGHT, buff=0.5)

        output_wire = Arrow(
            gate2.get_right(), output.get_left(), buff=0.1, color=ORANGE
        )

        self.play(Write(output), Create(output_wire))
        self.wait(1)

        # Animate the computation flow
        self.animate_computation_flow(
            gate1,
            gate2,
            connecting_wire,
            input_a_wire,
            input_b_wire,
            input_c_wire,
            output_wire,
        )

        # Show the garbling process
        self.explain_garbling(alice, bob, gate1, gate2)

        # Final explanation
        final_text = Text(
            "Chaining gates allows for complex secure computations", font_size=24
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

    def animate_computation_flow(
        self,
        gate1,
        gate2,
        connecting_wire,
        input_a_wire,
        input_b_wire,
        input_c_wire,
        output_wire,
    ):
        # Create signal dots
        signal_a = Circle(radius=0.15, color=GREEN, fill_opacity=0.8)
        signal_a.move_to(input_a_wire.get_start())

        signal_b = Circle(radius=0.15, color=BLUE, fill_opacity=0.8)
        signal_b.move_to(input_b_wire.get_start())

        # Animate inputs flowing into gate 1
        self.play(
            signal_a.animate.move_to(input_a_wire.get_end()),
            signal_b.animate.move_to(input_b_wire.get_end()),
        )

        # Process in gate 1
        self.play(
            signal_a.animate.move_to(gate1.get_center()),
            signal_b.animate.move_to(gate1.get_center()),
        )

        # Output from gate 1 becomes input to gate 2
        intermediate_signal = Circle(radius=0.15, color=YELLOW, fill_opacity=0.8)
        self.play(
            ReplacementTransform(
                VGroup(signal_a, signal_b),
                intermediate_signal.move_to(connecting_wire.get_start()),
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
            signal_c.animate.move_to(gate2.get_center()),
        )

        # Final output
        final_signal = Circle(radius=0.15, color=ORANGE, fill_opacity=0.8)
        self.play(
            ReplacementTransform(
                VGroup(intermediate_signal, signal_c),
                final_signal.move_to(output_wire.get_start()),
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
            width=10, height=3, stroke_opacity=0, fill_opacity=0
        )
        explanation_area.to_edge(DOWN, buff=1)

        # Step 1: Alice garbles the circuit
        step1 = Text("1. Alice garbles both gates with random labels", font_size=20)
        step1.move_to(explanation_area.get_top() + DOWN * 0.5)

        alice_arrow = CurvedArrow(
            alice.get_bottom() + DOWN * 0.2,
            gate1.get_top() + UP * 0.2,
            angle=-TAU / 6,
            color=WHITE,
        )

        self.play(Write(step1), Create(alice_arrow))
        self.wait(1)

        # Step 2: Alice sends garbled circuit to Bob
        step2 = Text(
            "2. Alice sends garbled circuit and her encrypted inputs to Bob",
            font_size=20,
        )
        step2.move_to(explanation_area.get_center())

        transfer_arrow = Arrow(alice.get_right(), bob.get_left(), buff=0.5, color=WHITE)

        self.play(Write(step2), Create(transfer_arrow))
        self.wait(1)

        # Step 3: Bob evaluates
        step3 = Text("3. Bob evaluates the circuit gate by gate", font_size=20)
        step3.move_to(explanation_area.get_bottom() + UP * 0.5)

        bob_arrow1 = CurvedArrow(
            bob.get_bottom() + DOWN * 0.2,
            gate1.get_top() + RIGHT * 1 + UP * 0.2,
            angle=TAU / 6,
            color=WHITE,
        )

        bob_arrow2 = CurvedArrow(
            bob.get_bottom() + DOWN * 0.2,
            gate2.get_top() + UP * 0.2,
            angle=TAU / 6,
            color=WHITE,
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
            FadeOut(bob_arrow2),
        )


class ObliviousTransferAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Oblivious Transfer (OT) Protocol", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Introduction text
        intro_text = Text(
            "A cryptographic primitive where the sender doesn't know which message was received",
            font_size=24,
        )
        intro_text.next_to(title, DOWN)
        self.play(Write(intro_text))
        self.wait(1)

        # Create the two parties
        sender = self.create_party("Alice (Sender)", LEFT * 4.5 + UP * 1.5)
        receiver = self.create_party("Bob (Receiver)", RIGHT * 4.5 + UP * 1.5)

        self.play(Create(sender), Create(receiver))
        self.wait(1)

        # Create messages
        messages = self.create_messages()
        messages.next_to(sender, DOWN, buff=0.8)

        self.play(Create(messages))

        # Show Bob's choice
        choice_text = Text("Bob wants to receive m₁", font_size=24, color=YELLOW)
        choice_text.next_to(receiver, DOWN, buff=0.8)

        choice_arrow = Arrow(
            receiver.get_bottom() + DOWN * 0.2,
            choice_text.get_top(),
            buff=0.1,
            color=YELLOW,
        )

        self.play(Write(choice_text), Create(choice_arrow))
        self.wait(1)

        # Highlight Bob's choice
        highlight = SurroundingRectangle(messages[1], color=YELLOW)
        self.play(Create(highlight))
        self.wait(1)

        # Show the challenge of OT
        challenge_text = Text(
            "Challenge: Bob should receive only m₁ without Alice knowing his choice",
            font_size=24,
        )
        challenge_text.to_edge(DOWN, buff=1)
        self.play(Write(challenge_text))
        self.wait(2)

        # Clean up for protocol steps
        self.play(
            FadeOut(challenge_text),
            FadeOut(highlight),
            FadeOut(choice_text),
            FadeOut(choice_arrow),
        )

        # Animate the OT protocol
        self.animate_ot_protocol(sender, receiver, messages)

        # Final explanation
        final_text = Text(
            "Oblivious Transfer is a fundamental building block for secure computation",
            font_size=24,
        )
        final_text.to_edge(DOWN, buff=1)
        self.play(Write(final_text))
        self.wait(2)

    def create_party(self, name, position):
        party = VGroup()

        # Create person icon
        head = Circle(radius=0.2, color=WHITE)
        body = Rectangle(height=0.6, width=0.4, color=WHITE)
        body.next_to(head, DOWN, buff=0.1)

        person = VGroup(head, body)
        person.move_to(position)

        # Add name label
        label = Text(name, font_size=20)
        label.next_to(person, DOWN, buff=0.2)

        party.add(person, label)
        return party

    def create_messages(self):
        messages = VGroup()

        # Create message boxes
        m0_box = Rectangle(height=0.8, width=1.2, color=WHITE)
        m0_box.set_fill(color=RED, opacity=0.2)
        m0_label = MathTex(r"m_0")
        m0_label.scale(0.5)
        m0_label.move_to(m0_box.get_center())
        m0 = VGroup(m0_box, m0_label)

        m1_box = Rectangle(height=0.8, width=1.2, color=WHITE)
        m1_box.set_fill(color=GREEN, opacity=0.2)
        m1_label = MathTex(r"m_1")
        m1_label.scale(0.5)
        m1_label.move_to(m1_box.get_center())
        m1 = VGroup(m1_box, m1_label)

        m2_box = Rectangle(height=0.8, width=1.2, color=WHITE)
        m2_box.set_fill(color=RED, opacity=0.2)
        m2_label = MathTex(r"m_2")
        m2_label.scale(0.5)
        m2_label.move_to(m2_box.get_center())
        m2 = VGroup(m2_box, m2_label)

        # Position messages side by side
        m0.next_to(ORIGIN, LEFT, buff=0.8)
        m1.move_to(ORIGIN)
        m2.next_to(ORIGIN, RIGHT, buff=0.8)

        messages.add(m0, m1, m2)

        # Add title
        messages_title = Text("Alice's Messages", font_size=20)
        messages_title.next_to(messages, UP, buff=0.3)
        messages.add(messages_title)

        return messages

    def animate_ot_protocol(self, sender, receiver, messages):
        step_text_font_size = 25

        # Step 1: Bob generates keys
        step1_text = Tex(
            r"1. Bob generates 3 public keys ($pk_0, pk_1, pk_2$)",
            font_size=step_text_font_size,
            stroke_color=YELLOW,
        )
        step1_text.center()

        key0 = Rectangle(height=0.5, width=0.5, color=RED)
        key0_label = MathTex(r"pk_0")
        key0_label.scale(0.5)
        key0_label.move_to(key0.get_center())
        pk0 = VGroup(key0, key0_label)

        key1 = Rectangle(height=0.5, width=0.5, color=GREEN)
        key1_label = MathTex(r"pk_1")
        key1_label.scale(0.5)
        key1_label.move_to(key1.get_center())
        pk1 = VGroup(key1, key1_label)

        key2 = Rectangle(height=0.5, width=0.5, color=RED)
        key2_label = MathTex(r"pk_2")
        key2_label.scale(0.5)
        key2_label.move_to(key2.get_center())
        pk2 = VGroup(key2, key2_label)

        # Position keys near Bob
        keys = VGroup(pk0, pk1, pk2)
        keys.arrange(RIGHT, buff=0.5)
        keys.next_to(receiver, DOWN, buff=1.5)

        # Add title
        keys_title = Text("Bob's Keys", font_size=20)
        keys_title.next_to(keys, UP, buff=0.3)
        # keys.add(keys_title)

        # Show Bob's choice (pk1 is the "real" key)
        choice_indicator = Text("(Bob knows the secret key only for pk₁)", font_size=16)
        choice_indicator.next_to(keys, DOWN, buff=0.3)

        self.play(Write(step1_text))
        self.play(Create(keys), Write(choice_indicator))
        self.wait(1)

        # Step 2: Bob sends all keys to Alice
        step2_text = Tex(
            r"2. Bob sends all public keys ($pk_0, pk_1, pk_2$) to Alice",
            font_size=step_text_font_size,
            stroke_color=YELLOW,
        )
        step2_text.move_to(step1_text.get_center())

        key_transfer = Arrow(
            receiver.get_center() + LEFT * 2,
            sender.get_center() + RIGHT * 2,
            buff=0.2,
            color=YELLOW_C,
            # stroke_opacity=0.5,  # Set the opacity to make the arrow less obstructive
        )

        self.play(ReplacementTransform(step1_text, step2_text), Create(key_transfer))

        # Animate keys moving to Alice
        keys_copy = keys.copy()
        self.play(keys_copy.animate.next_to(sender, DOWN, buff=2))
        self.wait(1)

        # Fade out the key transfer arrow before step 3
        self.play(FadeOut(key_transfer))

        # Step 3: Alice encrypts her messages
        step3_text = Tex(
            r"3. Alice encrypts each message with the corresponding key",
            font_size=step_text_font_size,
            stroke_color=YELLOW,
        )
        step3_text.move_to(step2_text.get_center())

        # Create encrypted messages
        enc_m0 = Rectangle(height=0.8, width=1.5, color=WHITE)
        enc_m0.set_fill(color=RED, opacity=0.2)
        enc_m0_label = MathTex(r"Enc(pk_0, m_0)")
        enc_m0_label.scale(0.5)
        enc_m0_label.move_to(enc_m0.get_center())
        encrypted_m0 = VGroup(enc_m0, enc_m0_label)

        enc_m1 = Rectangle(height=0.8, width=1.5, color=WHITE)
        enc_m1.set_fill(color=GREEN, opacity=0.2)
        enc_m1_label = MathTex(r"Enc(pk_1, m_1)")
        enc_m1_label.scale(0.5)
        enc_m1_label.move_to(enc_m1.get_center())
        encrypted_m1 = VGroup(enc_m1, enc_m1_label)

        enc_m2 = Rectangle(height=0.8, width=1.5, color=WHITE)
        enc_m2.set_fill(color=RED, opacity=0.2)
        enc_m2_label = MathTex(r"Enc(pk_2, m_2)")
        enc_m2_label.scale(0.5)
        enc_m2_label.move_to(enc_m2.get_center())
        encrypted_m2 = VGroup(enc_m2, enc_m2_label)

        # Position encrypted messages
        encrypted_messages = VGroup(encrypted_m0, encrypted_m1, encrypted_m2)
        encrypted_messages.arrange(RIGHT, buff=0.3)
        encrypted_messages.next_to(sender, DOWN, buff=3)
        # Adjust the scene's bottom edge instead of moving messages up
        self.camera.frame_height = 11  # Increase frame height to show more space below

        self.play(
            ReplacementTransform(step2_text, step3_text),
            FadeOut(messages),
            FadeOut(keys_copy),
        )

        # Show encryption process
        lock0 = solid.lock
        lock0.scale(0.3)
        lock0.next_to(encrypted_m0, UP, buff=0.2)

        lock1 = lock0.copy()
        lock1.next_to(encrypted_m1, UP, buff=0.2)

        lock2 = lock0.copy()
        lock2.next_to(encrypted_m2, UP, buff=0.2)

        self.play(
            Create(encrypted_messages),
            Write(lock0, run_time=2),
            Write(lock1, run_time=2),
            Write(lock2, run_time=2),
        )
        self.wait(1)

        # Step 4: Alice sends encrypted messages to Bob
        step4_text = Tex(
            r"4. Alice sends all encrypted messages to Bob",
            font_size=step_text_font_size,
            stroke_color=YELLOW,
        )
        step4_text.move_to(step3_text.get_center())

        message_transfer = Arrow(
            encrypted_messages.get_right() + RIGHT * 0.5,
            encrypted_messages.get_right() + RIGHT * 3.5,
            buff=0.2,
            color=YELLOW_C,
            stroke_opacity=0.5,  # Set the opacity to make the arrow less obstructive
        )

        self.play(
            ReplacementTransform(step3_text, step4_text), Create(message_transfer)
        )

        # Animate messages moving to Bob
        encrypted_messages_copy = encrypted_messages.copy()
        self.play(
            encrypted_messages_copy.animate.next_to(receiver, DOWN, buff=3),
            FadeOut(lock0),
            FadeOut(lock1),
        )
        self.wait(1)

        # Fade out the key transfer arrow before step 5
        self.play(FadeOut(message_transfer))

        # Step 5: Bob decrypts only one message
        step5_text = Tex(
            r"5. Bob can decrypt only $m_1$ using his secret key for $pk_1$",
            font_size=step_text_font_size,
            stroke_color=YELLOW,
        )
        step5_text.move_to(step4_text.get_center())

        # Show decryption process
        decrypt_fail = Text("x Can't Decrypt", font_size=18, color=RED)
        decrypt_fail.next_to(encrypted_messages_copy[0], DOWN, buff=0.2)
        decrypt_fail_2 = decrypt_fail.copy()
        decrypt_fail_2.next_to(encrypted_messages_copy[2], DOWN, buff=0.2)

        decrypt_success = Text("✓ Can Decrypt", font_size=18, color=GREEN)
        decrypt_success.next_to(encrypted_messages_copy[1], DOWN, buff=0.2)

        self.play(
            ReplacementTransform(step4_text, step5_text),
            Write(decrypt_success),
            Write(decrypt_fail),
            Write(decrypt_fail_2),
        )

        # Highlight the message Bob can decrypt
        highlight = SurroundingRectangle(encrypted_messages_copy[1], color=YELLOW)
        self.play(Create(highlight))
        self.wait(1)

        # Show final decrypted message
        decrypted_message = Rectangle(height=0.8, width=1.2, color=YELLOW)
        decrypted_message.set_fill(color=GREEN, opacity=0.3)
        decrypted_label = Text("m₁", font_size=24)
        decrypted_label.move_to(decrypted_message.get_center())
        final_message = VGroup(decrypted_message, decrypted_label)

        # Position the final message to the left of Bob
        final_message.next_to(receiver, DOWN, buff=0.2)

        # Show an arrow indicating the decryption process from the encrypted message to the final message
        decrypt_arrow = CurvedArrow(
            encrypted_messages_copy[1].get_top() + UP * 0.1,
            final_message.get_right() + RIGHT * 0.1,
            angle=TAU / 6,
            color=GREEN,
        )

        # Add a "decrypted" label next to the arrow
        decrypt_label = solid.unlock.copy()
        decrypt_label.scale(0.2)  # Make it smaller
        decrypt_label.set_color(GREEN)  # Set color to green
        # Position it at the midpoint of the curve
        midpoint = decrypt_arrow.point_from_proportion(0.5)
        decrypt_label.move_to(
            final_message.get_right() + RIGHT * 0.5
        )  # Offset to be visible next to the arrow

        self.play(Create(decrypt_arrow), Create(final_message), Write(decrypt_label))
        self.wait(1)

        # Step 6: Security properties
        step6_text = Text("Security Properties of OT:", font_size=20)
        step6_text.move_to(step5_text.get_center())

        property1 = Text(
            "• Alice doesn't learn which message Bob received", font_size=18
        )
        property1.next_to(step6_text, DOWN, buff=0.3)

        property2 = Text(
            "• Bob learns exactly one message and nothing about the others",
            font_size=18,
        )
        property2.next_to(property1, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(step5_text, step6_text),
            FadeOut(encrypted_messages),
            FadeOut(encrypted_messages_copy),
            FadeOut(highlight),
            FadeOut(decrypt_success),
            FadeOut(decrypt_fail),
            FadeOut(decrypt_fail_2),
            FadeOut(final_message),
            FadeOut(decrypt_arrow),
            FadeOut(decrypt_label),
            FadeOut(keys),
            FadeOut(choice_indicator),
        )

        self.play(Write(property1), Write(property2))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(step6_text), FadeOut(property1), FadeOut(property2))


class GarbledGateAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Garbled Gate in Two-Party Computation", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Introduction text
        intro_text = Text(
            "A garbled gate allows secure computation without revealing inputs",
            font_size=24,
        )
        intro_text.next_to(title, DOWN)
        self.play(Write(intro_text))
        self.wait(1)

        # Create Alice and Bob
        alice = self.create_party("Alice (Garbler)", LEFT * 5 + UP * 1.5)
        bob = self.create_party("Bob (Evaluator)", RIGHT * 5 + UP * 1.5)

        self.play(FadeIn(alice), FadeIn(bob))
        self.wait(1)

        # Create XOR gate
        xor_gate = self.create_xor_gate()
        xor_gate.scale(0.8)
        xor_gate.move_to(ORIGIN)

        self.play(Create(xor_gate))
        self.wait(1)

        # Show the truth table for XOR
        truth_table = self.create_truth_table()
        truth_table.scale(0.7)
        truth_table.to_edge(DOWN)

        self.play(Create(truth_table))
        self.wait(1)

        # Explain the garbling process
        garbled_table = self.explain_garbling_process(alice, bob, xor_gate, truth_table)

        # Explain the ElGamal encryption used
        self.explain_elgamal_encryption()

        # Show Bob evaluating the garbled gate
        self.show_evaluation(bob, xor_gate)

        # Conclusion
        conclusion = Text(
            "Garbled gates enable secure computation without revealing inputs",
            font_size=24,
        )
        conclusion.to_edge(DOWN)

        self.play(FadeOut(truth_table))
        self.play(Write(conclusion))
        self.wait(2)

    def create_party(self, name, position):
        # Create a character to represent a party
        body = Circle(radius=0.5, color=WHITE, fill_opacity=0.2)
        label = Text(name, font_size=20).next_to(body, DOWN)
        return VGroup(body, label).move_to(position)

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
        input_x = Text("x", font_size=24).next_to(input_line1, LEFT)
        input_y = Text("y", font_size=24).next_to(input_line2, LEFT)
        output = Text("output", font_size=24).next_to(output_line, RIGHT)

        return VGroup(
            gate_body,
            curve,
            input_line1,
            input_line2,
            output_line,
            input_x,
            input_y,
            output,
        )

    def create_truth_table(self):
        # From the code example: input_array = ["00", "01", "10", "11"]
        # plain_xor_gate_outputs = ["0", "1", "1", "0"]
        table = Table(
            [
                ["x", "y", "x ⊕ y"],
                ["0", "0", "0"],
                ["0", "1", "1"],
                ["1", "0", "1"],
                ["1", "1", "0"],
            ],
            include_outer_lines=True,
        )
        return table

    def explain_garbling_process(self, alice, bob, xor_gate, truth_table):
        # Step 1: Show Alice creating random keys for inputs
        step1_text = Text(
            "Step 1: Generate random keys for each input bit", font_size=24
        )
        step1_text.next_to(alice, RIGHT)

        self.play(Write(step1_text))
        self.wait(1)

        # Show the keys (using example values from the code)
        keys_text = [
            Text("Keys for x=0: P_x_0 (128-bit random value)", font_size=20),
            Text("Keys for x=1: P_x_1 (128-bit random value)", font_size=20),
            Text("Keys for y=0: P_y_0 (128-bit random value)", font_size=20),
            Text("Keys for y=1: P_y_1 (128-bit random value)", font_size=20),
        ]

        for i, key_text in enumerate(keys_text):
            key_text.next_to(alice, RIGHT + DOWN * (i * 0.5 + 1))
            self.play(Write(key_text))

        self.wait(1)

        # Step 2: Create the garbled table
        self.play(FadeOut(step1_text), *[FadeOut(key) for key in keys_text])

        step2_text = Text(
            "Step 2: Create the garbled table using ElGamal encryption", font_size=24
        )
        step2_text.next_to(alice, RIGHT)

        self.play(Write(step2_text))
        self.wait(1)

        # Show the garbled table creation process
        garbling_steps = [
            Text("1. For each input combination (x,y):", font_size=20),
            Text("2. Compute hash of input passwords as lookup key", font_size=20),
            Text("3. Encrypt output with combined password", font_size=20),
            Text("4. Store (hash_key, encrypted_output) in table", font_size=20),
        ]

        for i, step in enumerate(garbling_steps):
            step.next_to(step2_text, DOWN * (i + 1))
            self.play(Write(step))
            self.wait(0.5)

        self.wait(1)
        self.play(*[FadeOut(step) for step in garbling_steps])

        # Show the garbled table
        garbled_table = self.create_garbled_table()
        garbled_table.scale(0.7)
        garbled_table.next_to(xor_gate, RIGHT * 3)

        self.play(Create(garbled_table))
        self.wait(1)

        # Step 3: Send the garbled table to Bob
        self.play(FadeOut(step2_text))

        step3_text = Text("Step 3: Send garbled table to Bob", font_size=24)
        step3_text.next_to(alice, RIGHT)

        self.play(Write(step3_text))
        self.wait(1)

        # Animate sending the table to Bob
        garbled_table_copy = garbled_table.copy()
        self.play(garbled_table_copy.animate.next_to(bob, LEFT))
        self.wait(1)

        self.play(FadeOut(step3_text), FadeOut(garbled_table))

        return garbled_table_copy

    def create_garbled_table(self):
        # Create a representation of the garbled table with actual example values
        # From the code: for each input combination, we encrypt the output
        table = Table(
            [
                ["Hash(P_x_0, P_y_0)", "Enc_{P_x_0+P_y_0}('0')"],
                ["Hash(P_x_0, P_y_1)", "Enc_{P_x_0+P_y_1}('1')"],
                ["Hash(P_x_1, P_y_0)", "Enc_{P_x_1+P_y_0}('1')"],
                ["Hash(P_x_1, P_y_1)", "Enc_{P_x_1+P_y_1}('0')"],
            ],
            col_labels=[Text("Hash Key"), Text("Encrypted Output")],
            include_outer_lines=True,
        )

        # Highlight the rows to show they're randomly permuted
        colors = [BLUE, GREEN, YELLOW, RED]
        for i in range(4):
            table.add_highlighted_cell((i + 1, 1), color=colors[i], fill_opacity=0.2)
            table.add_highlighted_cell((i + 1, 2), color=colors[i], fill_opacity=0.2)

        return table

    def show_evaluation(self, bob, xor_gate):
        # Step 4: Bob receives input keys through OT
        step4_text = Text(
            "Step 4: Bob receives input keys via Oblivious Transfer", font_size=24
        )
        step4_text.next_to(bob, LEFT)

        self.play(Write(step4_text))
        self.wait(1)

        # Show Bob's inputs - using the example from the code (chosen_input = "11")
        input_text = Text("Bob's inputs: x=1, y=1", font_size=20)
        input_text.next_to(step4_text, DOWN)

        self.play(Write(input_text))
        self.wait(1)

        # Show the keys Bob received
        keys_received = Text("Keys received: P_x_1, P_y_1", font_size=20)
        keys_received.next_to(input_text, DOWN)

        self.play(Write(keys_received))
        self.wait(1)

        # Step 5: Bob evaluates the garbled gate
        self.play(FadeOut(step4_text), FadeOut(input_text), FadeOut(keys_received))

        step5_text = Text("Step 5: Bob evaluates the garbled gate", font_size=24)
        step5_text.next_to(bob, LEFT)

        self.play(Write(step5_text))
        self.wait(1)

        # Show the evaluation process with actual code example steps
        eval_steps = [
            Text("1. Compute hash_key = Hash(P_x_1, P_y_1)", font_size=20),
            Text("2. Find matching row in garbled table", font_size=20),
            Text("3. Compute decryption key = P_x_1 + P_y_1", font_size=20),
            Text("4. Decrypt Enc_{P_x_1+P_y_1}('0')", font_size=20),
            Text("5. Get result: 0", font_size=20),
        ]

        for i, step in enumerate(eval_steps):
            step.next_to(step5_text, DOWN * (i + 1))
            self.play(Write(step))
            self.wait(0.5)

        # Highlight the result
        result_circle = Circle(radius=0.3, color=RED, fill_opacity=0.8)
        result_circle.move_to(xor_gate[4].get_end())  # Position at output
        result_text = Text("0", font_size=24, color=WHITE).move_to(result_circle)

        self.play(Create(result_circle), Write(result_text))
        self.wait(1)

        # Show code verification
        verification = Text("Matches expected output: x⊕y = 1⊕1 = 0", font_size=20)
        verification.next_to(eval_steps[-1], DOWN)
        self.play(Write(verification))
        self.wait(1)

        # Clean up
        self.play(
            FadeOut(step5_text),
            *[FadeOut(step) for step in eval_steps],
            FadeOut(result_circle),
            FadeOut(result_text),
            FadeOut(verification)
        )

    def explain_elgamal_encryption(self):
        # Title for ElGamal section
        elgamal_title = Text("ElGamal Encryption in Garbled Gates", font_size=30)
        elgamal_title.to_edge(UP + DOWN * 0.5)

        self.play(Write(elgamal_title))
        self.wait(1)

        # Create a box to show the encryption process
        encryption_box = Rectangle(height=4, width=6, color=WHITE)
        encryption_box.move_to(ORIGIN)

        self.play(Create(encryption_box))

        # Show the ElGamal encryption steps
        elgamal_steps = [
            Text("ElGamal Encryption Process:", font_size=24),
            Text("1. Generate keys: (p, g, y=g^x mod p)", font_size=20),
            Text("2. Public key: (p, g, y)", font_size=20),
            Text("3. Private key: x", font_size=20),
            Text("4. Encrypt: c = (g^k mod p, m·y^k mod p)", font_size=20),
            Text("5. Decrypt: m = c2 · (c1^x)^(-1) mod p", font_size=20),
        ]

        # Position and animate the steps
        elgamal_steps[0].next_to(encryption_box, UP)
        self.play(Write(elgamal_steps[0]))

        for i in range(1, len(elgamal_steps)):
            elgamal_steps[i].move_to(encryption_box.get_center() + UP * (1.5 - i * 0.6))
            self.play(Write(elgamal_steps[i]))
            self.wait(0.5)

        self.wait(1)

        # Show example values from the code
        example_title = Text("Example from code:", font_size=24)
        example_title.next_to(encryption_box, DOWN)

        self.play(Write(example_title))

        # Show actual example values from the code
        example_values = [
            Text("For input (1,1):", font_size=20),
            Text("1. Hash key = hash(P_x_1, P_y_1)", font_size=20),
            Text("2. Password = P_x_1 + P_y_1 mod p", font_size=20),
            Text("3. Encrypt output '0' with password", font_size=20),
            Text("4. Store in garbled table", font_size=20),
        ]

        for i, value in enumerate(example_values):
            value.next_to(example_title, DOWN * (i + 1))
            self.play(Write(value))
            self.wait(0.5)

        self.wait(1)

        # Clean up
        self.play(
            FadeOut(elgamal_title),
            FadeOut(encryption_box),
            *[FadeOut(step) for step in elgamal_steps],
            FadeOut(example_title),
            *[FadeOut(value) for value in example_values]
        )


# if __name__ == "__main__":
#     config.pixel_height = 720
#     config.pixel_width = 1280
#     config.frame_rate = 30
#     scene = ObliviousTransferAnimation()
#     scene.render()
