import pygame
import sys
import os
import datetime

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Component classes
class Component:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.inputs = []
        self.outputs = []
        self.state = False
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN if self.state else RED, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render("1" if self.state else "0", True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def update(self):
        pass

    def start_drag(self, mouse_pos):
        self.dragging = True
        self.offset_x = self.rect.x - mouse_pos[0]
        self.offset_y = self.rect.y - mouse_pos[1]

    def end_drag(self):
        self.dragging = False

    def drag(self, mouse_pos):
        if self.dragging:
            self.rect.x = mouse_pos[0] + self.offset_x
            self.rect.y = mouse_pos[1] + self.offset_y

    def remove_connections(self):
        for input_component in self.inputs:
            input_component.outputs.remove(self)
        for output_component in self.outputs:
            output_component.inputs.remove(self)

class Input(Component):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, RED)

    def toggle(self):
        self.state = not self.state
        self.propagate()

    def propagate(self):
        for output in self.outputs:
            output.update()

class Gate(Component):
    def __init__(self, x, y, gate_type):
        super().__init__(x, y, 80, 60, BLUE)
        self.gate_type = gate_type
        self.max_inputs = 1 if gate_type in ["NOT", "BUFFER"] else 2

    def draw(self, screen):
        if self.gate_type in ["AND", "NAND"]:
            pygame.draw.line(screen, BLACK, (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), 2)
            pygame.draw.line(screen, BLACK, (self.rect.left, self.rect.top), (self.rect.centerx, self.rect.top), 2)
            pygame.draw.line(screen, BLACK, (self.rect.left, self.rect.bottom), (self.rect.centerx, self.rect.bottom), 2)
            pygame.draw.arc(screen, BLACK, (self.rect.left, self.rect.top, self.rect.width, self.rect.height), -1.57, 1.57, 2)
            if self.gate_type == "NAND":
                pygame.draw.circle(screen, BLACK, (self.rect.right + 5, self.rect.centery), 5)
        elif self.gate_type in ["OR", "NOR", "XOR", "XNOR"]:
            pygame.draw.arc(screen, BLACK, (self.rect.left - 40, self.rect.top, self.rect.width + 40, self.rect.height), -1.57, 1.57, 2)
            pygame.draw.arc(screen, BLACK, (self.rect.left - 20, self.rect.top, 40, self.rect.height), 1.57, 4.71, 2)
            if self.gate_type in ["NOR", "XNOR"]:
                pygame.draw.circle(screen, BLACK, (self.rect.right + 5, self.rect.centery), 5)
            if self.gate_type in ["XOR", "XNOR"]:
                pygame.draw.arc(screen, BLACK, (self.rect.left - 30, self.rect.top, 40, self.rect.height), 1.57, 4.71, 2)
        elif self.gate_type in ["NOT", "BUFFER"]:
            pygame.draw.polygon(screen, BLACK, [(self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), (self.rect.right - 10, self.rect.centery)], 2)
            if self.gate_type == "NOT":
                pygame.draw.circle(screen, BLACK, (self.rect.right, self.rect.centery), 5)

        # Draw input lines
        if self.gate_type not in ["NOT", "BUFFER"]:
            pygame.draw.line(screen, BLACK, (self.rect.left - 20, self.rect.top + self.rect.height * 0.25), (self.rect.left, self.rect.top + self.rect.height * 0.25), 2)
            pygame.draw.line(screen, BLACK, (self.rect.left - 20, self.rect.top + self.rect.height * 0.75), (self.rect.left, self.rect.top + self.rect.height * 0.75), 2)
        else:
            pygame.draw.line(screen, BLACK, (self.rect.left - 20, self.rect.centery), (self.rect.left, self.rect.centery), 2)
        
        # Draw output line
        pygame.draw.line(screen, BLACK, (self.rect.right, self.rect.centery), (self.rect.right + 20, self.rect.centery), 2)

        # Draw gate label
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate_type, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        # Draw truth table
        self.draw_truth_table(screen)

    def draw_truth_table(self, screen):
        font = pygame.font.Font(None, 20)
        table_width = 60
        table_height = 80 if self.max_inputs == 2 else 60
        table_left = self.rect.left + (self.rect.width - table_width) // 2
        table_top = self.rect.bottom + 10

        pygame.draw.rect(screen, WHITE, (table_left, table_top, table_width, table_height))
        pygame.draw.rect(screen, BLACK, (table_left, table_top, table_width, table_height), 1)

        truth_tables = {
            "AND": ["A B | Q", "0 0 | 0", "0 1 | 0", "1 0 | 0", "1 1 | 1"],
            "OR": ["A B | Q", "0 0 | 0", "0 1 | 1", "1 0 | 1", "1 1 | 1"],
            "NOT": ["A | Q", "0 | 1", "1 | 0"],
            "NAND": ["A B | Q", "0 0 | 1", "0 1 | 1", "1 0 | 1", "1 1 | 0"],
            "NOR": ["A B | Q", "0 0 | 1", "0 1 | 0", "1 0 | 0", "1 1 | 0"],
            "XOR": ["A B | Q", "0 0 | 0", "0 1 | 1", "1 0 | 1", "1 1 | 0"],
            "XNOR": ["A B | Q", "0 0 | 1", "0 1 | 0", "1 0 | 0", "1 1 | 1"],
            "BUFFER": ["A | Q", "0 | 0", "1 | 1"]
        }

        rows = truth_tables[self.gate_type]

        for i, row in enumerate(rows):
            bg_color = WHITE
            if i > 0:  # Skip header row
                if self.max_inputs == 2:
                    input_a = int(row[0])
                    input_b = int(row[2])
                    if len(self.inputs) == 2 and self.inputs[0].state == bool(input_a) and self.inputs[1].state == bool(input_b):
                        bg_color = YELLOW
                elif self.max_inputs == 1:
                    input_a = int(row[0])
                    if len(self.inputs) == 1 and self.inputs[0].state == bool(input_a):
                        bg_color = YELLOW

            pygame.draw.rect(screen, bg_color, (table_left, table_top + i * table_height // len(rows), table_width, table_height // len(rows)))
            text = font.render(row, True, BLACK)
            text_rect = text.get_rect(midleft=(table_left + 5, table_top + (i + 0.5) * table_height / len(rows)))
            screen.blit(text, text_rect)

    def update(self):
        if self.gate_type == "AND":
            self.state = len(self.inputs) == 2 and all(input.state for input in self.inputs)
        elif self.gate_type == "OR":
            self.state = len(self.inputs) > 0 and any(input.state for input in self.inputs)
        elif self.gate_type == "NOT":
            self.state = len(self.inputs) == 1 and not self.inputs[0].state
        elif self.gate_type == "NAND":
            self.state = not (len(self.inputs) == 2 and all(input.state for input in self.inputs))
        elif self.gate_type == "NOR":
            self.state = not (len(self.inputs) > 0 and any(input.state for input in self.inputs))
        elif self.gate_type == "XOR":
            self.state = len(self.inputs) == 2 and (self.inputs[0].state != self.inputs[1].state)
        elif self.gate_type == "XNOR":
            self.state = len(self.inputs) == 2 and (self.inputs[0].state == self.inputs[1].state)
        elif self.gate_type == "BUFFER":
            self.state = len(self.inputs) == 1 and self.inputs[0].state
        self.propagate()

    def propagate(self):
        for output in self.outputs:
            output.update()

class Output(Component):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, RED)

    def update(self):
        if self.inputs:
            self.state = any(input.state for input in self.inputs)

def draw_toolbar(screen):
    gate_types = ["INPUT", "AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR", "BUFFER", "OUTPUT", "SAVE", "PRINT"]
    colors = [RED, BLUE, GREEN, (255, 165, 0), (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 192, 203), (165, 42, 42), BLACK, (100, 100, 100), (150, 150, 150)]
    
    for i, (gate_type, color) in enumerate(zip(gate_types, colors)):
        pygame.draw.rect(screen, color, (i * 85, 0, 85, 50))
        font = pygame.font.Font(None, 24)
        text = font.render(gate_type, True, WHITE)
        text_rect = text.get_rect(center=(i * 85 + 42, 25))
        screen.blit(text, text_rect)

def save_diagram(screen):
    if not os.path.exists("saved_diagrams"):
        os.makedirs("saved_diagrams")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"saved_diagrams/diagram_{timestamp}.png"
    pygame.image.save(screen, filename)
    print(f"Diagram saved as {filename}")

def print_diagram(screen):
    import tempfile
    import subprocess

    # Save the screen to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        pygame.image.save(screen, tmp_file.name)

    # Open the image with the default image viewer (which usually allows printing)
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.call(('open', tmp_file.name))
    elif os.name == 'nt':  # Windows
        os.startfile(tmp_file.name)
    elif os.name == 'posix':  # Linux
        subprocess.call(('xdg-open', tmp_file.name))

    print("Opening diagram for printing. Please use your system's print dialog to print the diagram.")

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Logic Gate Designer")

    components = []
    connecting = False
    start_component = None
    dragging_component = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    if y < 50:  # Toolbar area
                        gate_types = ["INPUT", "AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR", "BUFFER", "OUTPUT", "SAVE", "PRINT"]
                        index = x // 85
                        if index < len(gate_types):
                            if gate_types[index] == "INPUT":
                                components.append(Input(x, 100))
                            elif gate_types[index] == "OUTPUT":
                                components.append(Output(x, 100))
                            elif gate_types[index] == "SAVE":
                                save_diagram(screen)
                            elif gate_types[index] == "PRINT":
                                print_diagram(screen)
                            elif index < 10:  # Other gates
                                components.append(Gate(x, 100, gate_types[index]))
                    else:
                        for component in components:
                            if component.rect.collidepoint(event.pos):
                                if not connecting:
                                    if isinstance(component, (Input, Gate)):
                                        connecting = True
                                        start_component = component
                                    component.start_drag(event.pos)
                                    dragging_component = component
                                else:
                                    if start_component != component and isinstance(component, (Gate, Output)):
                                        if component not in start_component.outputs and (not isinstance(component, Gate) or len(component.inputs) < component.max_inputs):
                                            start_component.outputs.append(component)
                                            component.inputs.append(start_component)
                                            start_component.update()  # Update the state after connection
                                    connecting = False
                                    start_component = None
                                break
                elif event.button == 3:  # Right click
                    connecting = False
                    start_component = None
                    for component in components:
                        if isinstance(component, Input) and component.rect.collidepoint(event.pos):
                            component.toggle()
                            break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging_component:
                        dragging_component.end_drag()
                        dragging_component = None
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging_component:
                    dragging_component.drag(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    mouse_pos = pygame.mouse.get_pos()
                    for component in components[:]:
                        if component.rect.collidepoint(mouse_pos):
                            component.remove_connections()
                            components.remove(component)
                            break

        screen.fill(WHITE)

        # Draw toolbar with labels
        draw_toolbar(screen)

        # Draw components and connections
        for component in components:
            component.draw(screen)
            if isinstance(component, (Input, Gate)):
                output_pos = (component.rect.right + 20, component.rect.centery)
            else:
                output_pos = component.rect.midright
            
            for output in component.outputs:
                if isinstance(output, Gate):
                    input_index = output.inputs.index(component)
                    if output.gate_type in ["NOT", "BUFFER"]:
                        input_pos = (output.rect.left - 20, output.rect.centery)
                    else:
                        input_pos = (output.rect.left - 20, output.rect.top + output.rect.height * (0.25 if input_index == 0 else 0.75))
                else:
                    input_pos = output.rect.midleft
                pygame.draw.line(screen, BLACK, output_pos, input_pos, 2)

        # Draw connection in progress
        if connecting and start_component:
            pygame.draw.line(screen, BLUE, (start_component.rect.right + 20, start_component.rect.centery), pygame.mouse.get_pos(), 2)

        pygame.display.flip()

if __name__ == "__main__":
    main()
