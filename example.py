from manim import *


class SquareToCircle(Scene):

    def construct(self) -> None:
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class FibonacciSequence(Scene):
    def construct(self) -> None:
        # Title
        title = Text("Fibonacci Sequence").scale(1.2).to_edge(UP)
        self.play(Write(title))
        
        # Formula
        formula = MathTex(r"F_n = F_{n-1} + F_{n-2}").next_to(title, DOWN)
        self.play(Write(formula))
        self.wait(1)
        
        # First 5 Fibonacci numbers: 1, 1, 2, 3, 5
        fib_numbers = [1, 1, 2, 3, 5]
        
        # Create squares to represent the numbers
        squares = []
        x_pos = -5
        
        # Create the first 5 squares with their values
        for i, num in enumerate(fib_numbers):
            square = Square(side_length=num)
            square.set_fill(BLUE, opacity=0.5)
            square.set_stroke(WHITE, width=2)
            
            # Position squares in a row
            square.move_to([x_pos + num/2, -1, 0])
            x_pos += num + 0.5
            
            # Add number label
            label = Text(str(num)).move_to(square.get_center())
            
            # Group square and label
            group = VGroup(square, label)
            squares.append(group)
        
        # Show the first two numbers
        self.play(Create(squares[0]))
        self.wait(0.5)
        self.play(Create(squares[1]))
        self.wait(1)
        
        # Show how each subsequent number is formed
        for i in range(2, 5):
            # Create arrows pointing to the new square
            arrow1 = Arrow(squares[i-2].get_top(), squares[i].get_bottom() + LEFT, buff=0.2)
            arrow2 = Arrow(squares[i-1].get_top(), squares[i].get_bottom() + RIGHT, buff=0.2)
            
            # Create equation for this step
            eq = MathTex(f"{fib_numbers[i-2]} + {fib_numbers[i-1]} = {fib_numbers[i]}")
            eq.next_to(squares[i], UP, buff=1)
            
            # Animate
            self.play(Create(arrow1), Create(arrow2))
            self.play(Write(eq))
            self.play(Create(squares[i]))
            self.wait(1)
            
            # Clean up for next iteration
            self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(eq))
        
        # Final explanation
        explanation = Text("Each number is the sum of the two preceding ones", 
                          font_size=24).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)
