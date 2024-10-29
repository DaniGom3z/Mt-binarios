import tkinter as tk
from tkinter import ttk

class BinaryTuringMachine:
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.current_state = 'q0'
        self.transitions = self.initialize_transitions()
        
    def initialize_transitions(self):
        return {
            ('q0', '1'): ('q1', '1', 'R'),
            ('q1', '0'): ('q2', '0', 'R'),
            ('q2', '+'): ('q3', '+', 'R'),
            ('q3', '0'): ('q3', '0', 'R'),
            ('q3', '1'): ('q3', '1', 'R'),
            ('q3', '='): ('q4', '=', 'R'),
            ('q4', ''): ('q5', '', 'S') 
        }
        
    def step(self):
        if self.head_position >= len(self.tape):
            self.tape.append('')
        
        current_symbol = self.tape[self.head_position]
        transition_key = (self.current_state, current_symbol)
        
        if transition_key not in self.transitions:
            return False
        
        new_state, write_symbol, movement = self.transitions[transition_key]
        self.tape[self.head_position] = write_symbol
        self.current_state = new_state
        
        if movement == 'R':
            self.head_position += 1
            
        return True
    
    def extract_numbers(self):
        tape_string = ''.join(self.tape)
        parts = tape_string.split('+')
        if len(parts) != 2:
            return None, None
            
        num1 = parts[0].strip()
        num2 = parts[1].split('=')[0].strip()
        return self.convert_to_decimal(num1), self.convert_to_decimal(num2)
    
    def convert_to_decimal(self, binary_string):
        try:
            return int(binary_string, 2)
        except ValueError:
            return None
    
    def calculate_sum(self):
        num1, num2 = self.extract_numbers()
        if num1 is None or num2 is None:
            return None
        return bin(num1 + num2)[2:]  # Elimina el prefijo '0b'
    
    def run(self, input_string):
        self.tape = list(input_string)
        self.head_position = 0
        self.current_state = 'q0'
        
        while self.step():
            if self.current_state == 'q5':
                return True
                
        return False


class SimpleBinaryTuringGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Máquina de Turing - Suma Binaria")
        self.root.geometry("500x150")
        self.root.configure(bg="#f0f0f0")

        self.turing_machine = BinaryTuringMachine()
        self.create_widgets()
        
    def create_widgets(self):
        self.input_var = tk.StringVar()
        
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=20)
        
        entry = tk.Entry(input_frame, textvariable=self.input_var, font=('Helvetica', 14), width=30)
        entry.pack(side=tk.LEFT, padx=10)
        
        calculate_button = tk.Button(input_frame, text="Calcular", command=self.run_machine, font=('Helvetica', 12))
        calculate_button.pack(side=tk.LEFT, padx=10)

        self.result_var = tk.StringVar()
        self.result_label = tk.Label(self.root, textvariable=self.result_var, font=('Helvetica', 12), bg="#f0f0f0")
        self.result_label.pack(pady=10)
    
    def run_machine(self):
        input_string = self.input_var.get()
        if not input_string:
            self.result_var.set("Por favor ingrese una expresión binaria")
            return
            
        try:
            is_valid = self.turing_machine.run(input_string)
            if is_valid:
                result = self.turing_machine.calculate_sum()
                if result:
                    self.result_var.set(f"Resultado: {result} (binario) = {int(result, 2)} (decimal)")
                else:
                    self.result_var.set("Error al calcular la suma")
            else:
                self.result_var.set("Expresión binaria inválida")
                
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

if __name__ == "__main__":
    app = SimpleBinaryTuringGUI()
    app.root.mainloop()
