from manim import *
from manim_fontawesome import solid

from util.intro import displayLogo, displayTitle
from util.utils import displayNumberPlane


class ObliviousTransferAnimation(Scene):
    def construct(self):

        # Show Coordinates
        # displayNumberPlane(self)

        # Display the logo
        displayLogo(self)

        # Display title and introduction
        displayTitle(
            self,
            "Oblivious Transfer",
            "Ensure receiver gets one value without sender knowing which one",
        )

        # Create the two parties
        sender = self.create_party("Alice (Sender)", LEFT * 4.5 + UP * 1.5)
        receiver = self.create_party("Bob (Receiver)", RIGHT * 4.5 + UP * 1.5)
        self.sender = sender
        self.receiver = receiver

        self.play(Create(sender), Create(receiver))
        self.wait(1)

        # Create messages
        messages = self.create_messages()
        messages.next_to(sender, DOWN, buff=1)
        self.messages = messages

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
            "Challenge: Bob should receive only m₁ without Alice knowing " "his choice",
            font_size=24,
            color=YELLOW,
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
        self.animate_ot_protocol()

        # Final explanation
        final_text = Text(
            "Oblivious Transfer is a fundamental building block for multi-party "
            "computation",
            font_size=24,
        )
        final_text.center()
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

    def animate_ot_protocol(self):

        STEP_TEXT_FONT_SIZE = 30

        # Step 1: Bob generates keys
        step1_text = Tex(
            r"1. Bob generates 3 public keys ($pk_0, pk_1, pk_2$)",
            font_size=STEP_TEXT_FONT_SIZE,
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
        keys.next_to(self.receiver, DOWN, buff=1.5)

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
            font_size=STEP_TEXT_FONT_SIZE,
        )
        step2_text.move_to(step1_text.get_center())

        key_transfer = Arrow(
            self.receiver.get_center() + LEFT * 2,
            self.sender.get_center() + RIGHT * 2,
            buff=0.2,
            color=YELLOW_C,
        )

        self.play(ReplacementTransform(step1_text, step2_text), Create(key_transfer))

        # Animate keys moving to Alice
        keys_copy = keys.copy()
        self.play(keys_copy.animate.next_to(self.sender, DOWN, buff=2))
        self.wait(1)

        # Fade out the key transfer arrow before step 3
        self.play(FadeOut(key_transfer))

        # Step 3: Alice encrypts her messages
        step3_text = Tex(
            r"3. Alice encrypts each message with the corresponding key",
            font_size=STEP_TEXT_FONT_SIZE,
        )
        step3_text.move_to(step2_text.get_center())

        # Create encrypted messages
        enc_m0 = Rectangle(height=0.8, width=1.4, color=WHITE)
        enc_m0.set_fill(color=RED, opacity=0.2)
        enc_m0_label = MathTex(r"Enc(pk_0, m_0)")
        enc_m0_label.scale(0.4)
        enc_m0_label.move_to(enc_m0.get_center())
        encrypted_m0 = VGroup(enc_m0, enc_m0_label)

        enc_m1 = enc_m0.copy()
        enc_m1.set_fill(color=GREEN, opacity=0.2)
        enc_m1_label = enc_m0_label.copy()
        enc_m1_label.move_to(enc_m1.get_center())
        encrypted_m1 = VGroup(enc_m1, enc_m1_label)

        enc_m2 = enc_m0.copy()
        enc_m2_label = enc_m0_label.copy()
        enc_m2_label.move_to(enc_m2.get_center())
        encrypted_m2 = VGroup(enc_m2, enc_m2_label)

        # Position encrypted messages
        encrypted_messages = VGroup(encrypted_m0, encrypted_m1, encrypted_m2)
        encrypted_messages.arrange(RIGHT, buff=0.3)
        encrypted_messages.next_to(self.sender, DOWN, buff=1.5)
        # Adjust the scene's bottom edge instead of moving messages up
        self.camera.frame_height = 11  # Increase frame height

        self.play(
            ReplacementTransform(step2_text, step3_text),
            FadeOut(keys_copy),
        )

        # Show encryption process
        lock0 = solid.lock
        lock0.scale(0.2)
        lock0.next_to(encrypted_m0, DOWN, buff=0.2)

        lock1 = lock0.copy()
        lock1.next_to(encrypted_m1, DOWN, buff=0.2)

        lock2 = lock0.copy()
        lock2.next_to(encrypted_m2, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(self.messages, encrypted_messages),
            Write(lock0, run_time=3),
            Write(lock1, run_time=3),
            Write(lock2, run_time=3),
        )
        self.wait(2)

        # Step 4: Alice sends encrypted messages to Bob
        step4_text = Tex(
            r"4. Alice sends all encrypted messages to Bob",
            font_size=STEP_TEXT_FONT_SIZE,
        )
        step4_text.move_to(step3_text.get_center())

        message_transfer = Arrow(
            encrypted_messages.get_right() + RIGHT * 0.5,
            encrypted_messages.get_right() + RIGHT * 3.5,
            buff=0.2,
            color=YELLOW_C,
            stroke_opacity=0.5,
        )

        self.play(
            ReplacementTransform(step3_text, step4_text), Create(message_transfer)
        )

        # Animate messages moving to Bob
        encrypted_messages_copy = encrypted_messages.copy()
        self.play(
            encrypted_messages_copy.animate.next_to(self.receiver, DOWN, buff=3),
            FadeOut(lock0),
            FadeOut(lock1),
        )
        self.wait(1)

        # Fade out the key transfer arrow before step 5
        self.play(FadeOut(message_transfer))

        # Step 5: Bob decrypts only one message
        step5_text = Tex(
            r"5. Bob can decrypt only $m_1$ using his secret key for $pk_1$",
            font_size=STEP_TEXT_FONT_SIZE,
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
        final_message.next_to(self.receiver, DOWN, buff=0.2)

        # Show an arrow indicating the decryption process
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
        decrypt_label.move_to(
            final_message.get_right() + RIGHT * 0.5
        )  # Offset to be visible next to the arrow

        self.play(Create(decrypt_arrow), Create(final_message), Write(decrypt_label))
        self.wait(1)

        # Step 6: Security properties
        step6_text = Text("Security Properties of OT:", font_size=25)
        step6_text.center().move_to(UP * 0.5)

        property1 = Text(
            "• Alice doesn't learn which message Bob received", font_size=22
        )
        property1.next_to(step6_text, DOWN, buff=0.3)

        property2 = Text(
            "• Bob learns exactly one message and nothing about the others",
            font_size=22,
        )
        property2.next_to(property1, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(step5_text, step6_text),
            FadeOut(self.sender),
            FadeOut(self.receiver),
            FadeOut(self.messages),
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
        self.wait(4)

        # Cleanup
        self.play(FadeOut(step6_text), FadeOut(property1), FadeOut(property2))


class SingleGarbledGateAnimation(MovingCameraScene):
    def construct(self):

        self.STEP_TEXT_FONT_SIZE = 30
        self.STEP_TEXT_BUFF = 0.6

        # Show Coordinates
        # displayNumberPlane(self)

        # Display the logo
        displayLogo(self)

        # Display title and introduction
        displayTitle(
            self,
            "Garbled Gate",
            "A gate that hides its inputs and functionality",
        )

        # Create the two parties
        alice = self.create_party("Alice (Garbler)", LEFT * 5 + UP * 2.5)
        bob = self.create_party("Bob (Evaluator)", RIGHT * 5 + UP * 2.5)
        self.alice = alice
        self.bob = bob

        self.play(Create(alice), Create(bob))
        self.wait(1)

        # Step 1: Create AND gate
        self.animate_gate_creation()

        # Step 2: Alice garbles the gate
        self.animate_garbling()

        # Step 3: Alice sends garbled gate and labels to Bob
        self.animate_gate_transfer()

        # Step 4: Bob evaluates the garbled gate
        self.animate_evaluation()

        # Final explanation
        final_text_1 = Text(
            "Garbled circuits with oblivious transfer enable ",
            font_size=30,
        )
        final_text_2 = Text(
            "secure multi-party computation without revealing inputs",
            font_size=30,
        )
        final_text_group = VGroup(final_text_1, final_text_2)
        final_text_group.arrange(DOWN, buff=0.25)
        final_text_group.center()
        self.play(Write(final_text_group))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(final_text_group))

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

    def create_and_gate(self, position):
        # Create AND gate symbol
        gate = VGroup()
        # Gate body
        body = Rectangle(height=1.2, width=1.5, color=WHITE)
        body.set_fill(color=GREEN, opacity=0.2)
        # Gate label
        label = Text("AND", font_size=24)
        label.move_to(body.get_center())
        # Input wires
        input_a = Line(LEFT * 1.5, LEFT * 0.75, color=WHITE)
        input_a.move_to(body.get_left() + UP * 0.3)
        input_b = Line(LEFT * 1.5, LEFT * 0.75, color=WHITE)
        input_b.move_to(body.get_left() + DOWN * 0.3)
        # Output wire
        output = Line(RIGHT * 0.75, RIGHT * 1.5, color=WHITE)
        output.move_to(body.get_right())
        # Input labels
        label_a = Text("A", font_size=20)
        label_a.next_to(input_a, LEFT, buff=0.2)
        label_b = Text("B", font_size=20)
        label_b.next_to(input_b, LEFT, buff=0.2)
        # Output label
        label_out = Text("A∧B", font_size=20)
        label_out.next_to(output, RIGHT, buff=0.2)
        gate.add(body, label, input_a, input_b, output, label_a, label_b, label_out)
        gate.move_to(position)
        return gate

    def create_truth_table(self, position):
        # Create a truth table for AND gate
        table = VGroup()
        # Table headers
        header_a = Text("A", font_size=20)
        header_b = Text("B", font_size=20)
        header_out = Text("A∧B", font_size=20)
        # Table rows
        row1_a = Text("0", font_size=20)
        row1_b = Text("0", font_size=20)
        row1_out = Text("0", font_size=20)
        row2_a = Text("0", font_size=20)
        row2_b = Text("1", font_size=20)
        row2_out = Text("0", font_size=20)
        row3_a = Text("1", font_size=20)
        row3_b = Text("0", font_size=20)
        row3_out = Text("0", font_size=20)
        row4_a = Text("1", font_size=20)
        row4_b = Text("1", font_size=20)
        row4_out = Text("1", font_size=20)
        # Arrange headers
        headers = VGroup(header_a, header_b, header_out)
        headers.arrange(RIGHT, buff=0.5)
        # Arrange rows
        row1 = VGroup(row1_a, row1_b, row1_out)
        row1.arrange(RIGHT, buff=0.5)
        row1.next_to(headers, DOWN, buff=0.3)
        row2 = VGroup(row2_a, row2_b, row2_out)
        row2.arrange(RIGHT, buff=0.5)
        row2.next_to(row1, DOWN, buff=0.3)
        row3 = VGroup(row3_a, row3_b, row3_out)
        row3.arrange(RIGHT, buff=0.5)
        row3.next_to(row2, DOWN, buff=0.3)
        row4 = VGroup(row4_a, row4_b, row4_out)
        row4.arrange(RIGHT, buff=0.5)
        row4.next_to(row3, DOWN, buff=0.3)
        # Add all elements to the table
        table.add(headers, row1, row2, row3, row4)
        # Add a border around the table
        border = SurroundingRectangle(table, color=WHITE, buff=0.2)
        table.add(border)
        table.scale(0.8)
        table.move_to(position)
        return table

    def create_garbled_table(self, position):
        # Create a garbled table
        garbled_table = VGroup()
        # Table title
        title = Text("Garbled Truth Table", font_size=24)
        # Create encrypted entries
        entry1 = Rectangle(height=0.6, width=2.5, color=WHITE)
        entry1.set_fill(color=RED, opacity=0.2)
        entry1_label = Tex(r"$(0,0) | Enc_{P_{0,0}}(G(0,0))$", font_size=22)
        entry1_label.move_to(entry1.get_center())
        entry1_group = VGroup(entry1, entry1_label)
        entry2 = Rectangle(height=0.6, width=2.5, color=WHITE)
        entry2.set_fill(color=RED, opacity=0.2)
        entry2_label = Tex(r"$(0,1) | Enc_{P_{0,1}}(G(0,1))$", font_size=22)
        entry2_label.move_to(entry2.get_center())
        entry2_group = VGroup(entry2, entry2_label)
        entry3 = Rectangle(height=0.6, width=2.5, color=WHITE)
        entry3.set_fill(color=RED, opacity=0.2)
        entry3_label = Tex(r"$(1,0) | Enc_{P_{1,0}}(G(1,0))$", font_size=22)
        entry3_label.move_to(entry3.get_center())
        entry3_group = VGroup(entry3, entry3_label)
        entry4 = Rectangle(height=0.6, width=2.5, color=WHITE)
        entry4.set_fill(color=GREEN, opacity=0.2)
        entry4_label = Tex(r"$(1,1) | Enc_{P_{1,1}}(G(1,1))$", font_size=22)
        entry4_label.move_to(entry4.get_center())
        entry4_group = VGroup(entry4, entry4_label)
        # Arrange entries
        entries = VGroup(entry1_group, entry2_group, entry3_group, entry4_group)
        entries.arrange(DOWN, buff=0.3)
        # Add title above entries
        title.next_to(entries, UP, buff=0.3)
        # Add all elements to the garbled table
        garbled_table.add(title, entries)
        # Add a border around the table
        border = SurroundingRectangle(garbled_table, color=WHITE, buff=0.2)
        garbled_table.add(border)
        garbled_table.scale(0.8)
        garbled_table.move_to(position)
        return garbled_table

    def create_label_mapping(self, position):
        # Create a mapping of wire labels
        mapping = VGroup()
        # Title
        title = Text("Wire Label Mapping", font_size=24)
        # Create mappings
        map_a0 = Text("A=0 → k₀ᵃ", font_size=18)
        map_a1 = Text("A=1 → k₁ᵃ", font_size=18)
        map_b0 = Text("B=0 → k₀ᵇ", font_size=18)
        map_b1 = Text("B=1 → k₁ᵇ", font_size=18)
        map_out0 = Text("OUT=0 → k₀ᵒᵘᵗ", font_size=18)
        map_out1 = Text("OUT=1 → k₁ᵒᵘᵗ", font_size=18)
        # Arrange mappings
        input_maps = VGroup(map_a0, map_a1, map_b0, map_b1)
        input_maps.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        output_maps = VGroup(map_out0, map_out1)
        output_maps.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        output_maps.next_to(input_maps, DOWN, buff=0.5)
        # Add title above mappings
        title.next_to(VGroup(input_maps, output_maps), UP, buff=0.3)
        # Add all elements to the mapping
        mapping.add(title, input_maps, output_maps)
        # Add a border around the mapping
        border = SurroundingRectangle(mapping, color=WHITE, buff=0.2)
        mapping.add(border)
        mapping.scale(0.8)
        mapping.move_to(position)
        return mapping

    def animate_gate_creation(self):
        step_text = Text(
            "Step 1: Alice creates an AND gate",
            font_size=self.STEP_TEXT_FONT_SIZE,
        )
        step_text.to_edge(DOWN, buff=self.STEP_TEXT_BUFF)
        self.play(Write(step_text))
        # Create AND gate
        gate = self.create_and_gate(LEFT * 2)
        # Create truth table
        truth_table = self.create_truth_table(RIGHT * 2)
        # Show Alice creating the gate and truth table
        self.play(Create(gate), Create(truth_table))
        self.wait(1)
        # Move gate and truth table to Alice
        self.play(
            gate.animate.next_to(self.alice, DOWN * 0.5, buff=1),
            truth_table.animate.next_to(self.alice, DOWN * 2, buff=1),
            # FadeOut(truth_table),
        )
        self.wait(1)
        # Store gate and truth table for later use
        self.gate = gate
        self.truth_table = truth_table
        # Clean up
        self.play(FadeOut(step_text))

    def animate_garbling(self):
        step_text = Text(
            "Step 2: Alice garbles the gate by encrypting the input labels and outputs",
            font_size=self.STEP_TEXT_FONT_SIZE,
        )
        step_text.to_edge(DOWN, buff=self.STEP_TEXT_BUFF)
        self.play(Write(step_text))

        # Make AND gate smaller and move it closer to Alice
        self.play(self.gate.animate.set_fill(color=RED))
        self.play(self.gate.animate.scale(0.5))
        self.play(self.gate.animate.next_to(self.alice, DOWN, buff=0.5))
        self.wait(1)

        # Create garbled table
        garbled_table = self.create_garbled_table(UP * 1)
        # Show Alice creating the garbled table and label mapping
        self.play(
            ReplacementTransform(self.truth_table, garbled_table),
        )
        self.wait(1)
        # Move garbled table and label mapping to Alice
        self.play(
            garbled_table.animate.scale(0.7),
            # label_mapping.animate.scale(0.5),
        )
        # self.play(
        # label_mapping.animate.next_to(alice, DOWN * 6),
        # )
        # self.play(
        # label_mapping.animate.move_to(label_mapping.get_center() + LEFT * 0.5),
        # )
        self.play(
            # move the garbled table to the center of the scene
            garbled_table.animate.next_to(self.alice, DOWN * 6),
        )
        self.wait(1)
        # Store garbled table and label mapping for later use
        self.garbled_table = garbled_table
        # self.label_mapping = label_mapping
        # Clean up
        self.play(FadeOut(step_text))

    def animate_gate_transfer(self):
        step_text = Text(
            "Step 3: Alice sends the garbled gate to Bob",
            font_size=self.STEP_TEXT_FONT_SIZE,
        )
        step_text.to_edge(DOWN, buff=self.STEP_TEXT_BUFF)
        self.play(Write(step_text))
        # Create arrows for transfer
        gate_arrow = Arrow(
            self.alice.get_right() + RIGHT * 0.5,
            self.bob.get_left() + LEFT * 0.5,
            buff=0.2,
            color=YELLOW_C,
        )

        # Show transfer
        self.play(Create(gate_arrow))
        # Copy gate and garbled table to Bob
        gate_copy = self.gate.copy()
        garbled_table_copy = self.garbled_table.copy()
        self.play(
            gate_copy.animate.next_to(self.bob, DOWN, buff=0.5),
            garbled_table_copy.animate.next_to(self.bob, DOWN * 6),
        )
        self.wait(1)
        # Store Bob's copies
        self.bob_gate = gate_copy
        self.bob_garbled_table = garbled_table_copy
        # Clean up
        self.play(
            FadeOut(step_text),
            FadeOut(gate_arrow),
        )

    def animate_evaluation(self):
        step_text = Text(
            "Step 4: Bob evaluates the garbled gate with his inputs",
            font_size=self.STEP_TEXT_FONT_SIZE,
        )
        step_text.to_edge(DOWN, buff=self.STEP_TEXT_BUFF)
        self.play(Write(step_text))
        # Create Bob's input labels
        input_a = Text("Input A=1", font_size=20, color=YELLOW)
        input_a.next_to(self.bob_gate, LEFT + UP * 0.5, buff=0.1)
        input_b = Text("Input B=1", font_size=20, color=YELLOW)
        input_b.next_to(self.bob_gate, LEFT + DOWN * 0.5, buff=0.1)
        # Show Bob's inputs
        self.play(Write(input_a), Write(input_b))
        self.wait(1)
        # Highlight the corresponding entry in the garbled table (entry4)
        highlight = SurroundingRectangle(self.bob_garbled_table[1][3], color=YELLOW)
        self.play(Create(highlight))
        self.wait(1)

        # Show final output
        self.play(
            self.bob.animate.move_to(self.bob.get_center() + LEFT * 2),
            input_a.animate.move_to(input_a.get_center() + LEFT * 2),
            input_b.animate.move_to(input_b.get_center() + LEFT * 2),
            highlight.animate.move_to(highlight.get_center() + LEFT * 2),
            self.bob_gate.animate.move_to(self.bob_gate.get_center() + LEFT * 2),
            self.bob_garbled_table.animate.move_to(
                self.bob_garbled_table.get_center() + LEFT * 2
            ),
        )
        self.wait(1)

        # Show Bob decrypting the output
        decrypt_text = Text("Decrypt to get G(1,1)", font_size=20, color=GREEN)
        decrypt_text.next_to(highlight, RIGHT, buff=0.5)
        self.play(Write(decrypt_text))
        self.wait(1)

        # Show the decrypted output
        output_text = Text("Output: A∧B = 1", font_size=18, color=GREEN)
        output_text.next_to(self.bob, RIGHT, buff=0)
        output_arrow = CurvedArrow(
            self.bob_garbled_table.get_right() + RIGHT * 0.5,
            self.bob_garbled_table.get_right() + RIGHT * 0.5 + UP * 3,
            color=GREEN,
        )
        # Add a "decrypted" label next to the arrow
        decrypt_label = solid.unlock.copy()
        decrypt_label.scale(0.2)  # Make it smaller
        decrypt_label.set_color(GREEN)  # Set color to green
        # Position it at the midpoint of the curve
        decrypt_label.move_to(
            output_arrow.get_right() + RIGHT * 0.5
        )  # Offset to be visible next to the arrow

        self.play(
            Create(output_arrow),
            Write(output_text),
            Create(decrypt_label),
        )
        self.wait(1)

        # Explain security properties
        security_text1 = Text(
            "Bob learns only the output for his inputs. Alice doesn't learn Bob's inputs",
            font_size=27,
        )
        security_text1.to_edge(DOWN, buff=self.STEP_TEXT_BUFF)
        self.play(ReplacementTransform(step_text, security_text1))
        self.wait(4)
        # Clean up
        self.play(
            FadeOut(input_a),
            FadeOut(input_b),
            FadeOut(highlight),
            FadeOut(decrypt_text),
            FadeOut(output_text),
            FadeOut(output_arrow),
            FadeOut(decrypt_label),
            FadeOut(security_text1),
            FadeOut(self.gate),
            FadeOut(self.garbled_table),
            FadeOut(self.bob_gate),
            FadeOut(self.bob_garbled_table),
            FadeOut(self.alice),
            FadeOut(self.bob),
        )
