import tkinter as tk
import random
import math
import time

class ClosestPairNightModeApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2e2e2e")

        self.main_frame = tk.Frame(root, bg="#2e2e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=1920, height=500, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()

        self.controls_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.controls_frame.pack(fill=tk.X, pady=5)

        self.create_input_and_buttons()
        self.create_points(10)  

    def create_input_and_buttons(self):
        self.entry = tk.Entry(self.controls_frame, bg="#3c3c3c", fg="white", insertbackground="white", relief="flat")
        self.entry.pack(pady=5)
        set_button = tk.Button(self.controls_frame, text="Set Number of Points", command=self.set_number_of_black_points,
                               bg="#444", fg="white", activebackground="#555", activeforeground="white", relief="flat")
        set_button.pack(pady=5)

        button_frame = tk.Frame(self.controls_frame, bg="#2e2e2e")
        button_frame.pack(pady=5)

        play_button = tk.Button(button_frame, text="Play", command=self.find_and_draw_closest_pair,
                                bg="#444", fg="white", activebackground="#555", activeforeground="white", relief="flat")
        play_button.pack(side="left", padx=5)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_canvas,
                                 bg="#444", fg="white", activebackground="#555", activeforeground="white", relief="flat")
        reset_button.pack(side="left", padx=5)

        self.output_box = tk.Text(self.controls_frame, height=6, width=100, bg="#1e1e1e", fg="white", relief="flat",
                                  insertbackground="white")
        self.output_box.pack(pady=10)
        self.output_box.insert(tk.END, "Coordinates of the closest pair of points will appear here.\n")

    def create_points(self, num_black_points):
        start_time = time.perf_counter()  
        self.canvas.delete("all")
        self.black_points = []
        self.highlighted_circles = []  

        for _ in range(num_black_points):
            x, y = random.randint(25, 1500), random.randint(25, 475)  
            point = self.canvas.create_oval(x-1.5, y-1.5, x+1.5, y+1.5, fill="white", outline="white", tags="black")
            self.black_points.append(point)
            self.canvas.tag_bind(point, "<B1-Motion>", self.drag)

        end_time = time.perf_counter()  
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.output_box.insert(tk.END, f"Time to generate points: {elapsed_time:.6f} ms\n")

    def drag(self, event):
        widget = event.widget
        x, y = event.x, event.y
        widget.coords(tk.CURRENT, x-1.5, y-1.5, x+1.5, y+1.5)

    def find_and_draw_closest_pair(self):
        start_time = time.perf_counter()  
        self.canvas.delete("line")  
        for circle in self.highlighted_circles:
            self.canvas.delete(circle)  

        min_distance=float("inf")
        closest_pair=(None, None)

        for i in range(len(self.black_points)):
            for j in range(i + 1, len(self.black_points)):
                point1 = self.black_points[i]
                point2 = self.black_points[j]
                coords1 = self.canvas.coords(point1)
                coords2 = self.canvas.coords(point2)

                x1 = (coords1[0] + coords1[2]) / 2
                y1 = (coords1[1] + coords1[3]) / 2
                x2 = (coords2[0] + coords2[2]) / 2
                y2 = (coords2[1] + coords2[3]) / 2

                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = ((x1, y1), (x2, y2), point1, point2)

        if closest_pair[0] and closest_pair[1]:
            self.canvas.itemconfig( closest_pair[2] , fill="red" , outline="red")
            self.canvas.itemconfig( closest_pair[3] , fill="red" , outline="red")

    
            r = 10
            circle1 = self.canvas.create_oval(closest_pair[0][0]-r , closest_pair[0][1]-r, 
                                              closest_pair[0][0]+r , closest_pair[0][1]+r, 
                                              outline="red" , width=2 , tags="highlight")
            circle2 = self.canvas.create_oval(closest_pair[1][0]-r , closest_pair[1][1]-r, 
                                              closest_pair[1][0]+r , closest_pair[1][1]+r, 
                                              outline="red" , width=2 , tags="highlight")
            self.highlighted_circles.extend([circle1, circle2])

            
            self.canvas.create_line(closest_pair[0][0] , closest_pair[0][1] , closest_pair[1][0] , closest_pair[1][1] , fill="cyan" , width=2 , tags="line")

            
            end_time = time.perf_counter()  
            elapsed_time = (end_time-start_time)*1000  

            self.output_box.delete(1.0, tk.END)
            self.output_box.insert( tk.END, f"Point 1 (x, y): ({closest_pair[0][0]:.2f}, {closest_pair[0][1]:.2f})\n")
            self.output_box.insert( tk.END, f"Point 2 (x, y): ({closest_pair[1][0]:.2f}, {closest_pair[1][1]:.2f})\n")
            self.output_box.insert( tk.END, f"Distance: {min_distance:.2f}\n")
            self.output_box.insert( tk.END, f"Time to find closest pair: {elapsed_time:.6f} ms\n")

    def set_number_of_black_points(self):
        try:
            num_points = int( self.entry.get())
            if num_points <= 0:
                raise ValueError( "Number of points must be positive.")
            self.create_points( num_points)
        except ValueError as e:
            self.output_box.delete(1.0 , tk.END)
            self.output_box.insert(tk.END , f"Invalid input: {e}")

    def reset_canvas(self):
        self.create_points(10)
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert( tk.END, "Coordinates of the closest pair of points will appear here.\n")

        for point in self.black_points:
            self.canvas.itemconfig(point , fill="white", outline="white")
        for circle in self.highlighted_circles:
            self.canvas.delete(circle)
        self.highlighted_circles.clear()

if __name__ == "__main__":
    root=tk.Tk()
    app=ClosestPairNightModeApp(root)
    root.mainloop()
