import tkinter as tk
import random
import math
import time

class ClosestPairNightModeApp:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2e2e2e")

        self.main_frame=tk.Frame(root, bg="#2e2e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas= tk.Canvas(self.main_frame,width=1920,height=500, bg="#1e1e1e" , highlightthickness=0)
        self.canvas.pack()

        self.controls_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.controls_frame.pack(fill=tk.X, pady=5)

        self.create_input_and_buttons()
        self.create_points(10)

    def create_input_and_buttons(self):
        self.entry =tk.Entry(self.controls_frame , bg="#3c3c3c", fg="white",insertbackground="white", relief="flat")
        self.entry.pack(pady=5)
        set_button=tk.Button(self.controls_frame, text="Set Number of Points", command=self.set_number_of_black_points,
                               bg="#444", fg="white", activebackground="#555", activeforeground="white", relief="flat")
        set_button.pack(pady=5)

        button_frame=tk.Frame(self.controls_frame, bg="#2e2e2e")
        button_frame.pack(pady=5)

        play_button =tk.Button(button_frame, text="Play", command=self.find_and_draw_closest_pair,
                                bg="#444", fg="white", activebackground="#555" , activeforeground="white", relief="flat")
        play_button.pack(side="left", padx=5)

        reset_button= tk.Button(button_frame, text="Reset", command=self.reset_canvas,
                                 bg="#444", fg="white" , activebackground="#555", activeforeground="white",relief="flat")
        reset_button.pack(side="left", padx=5)

        self.output_box = tk.Text(self.controls_frame, height=6, width=100, bg="#1e1e1e", fg="white", relief="flat",
                                  insertbackground="white")
        self.output_box.pack(pady=10)
        self.output_box.insert(tk.END, "Coordinates of the closest pair of points will appear here.\n")

    def create_points(self, num_black_points):
        start_time= time.perf_counter()
        self.canvas.delete("all")
        self.black_points =[]
        self.highlighted_circles =[]

        for _ in range(num_black_points):
            x, y=random.randint(25, 1500), random.randint(25, 475)
            point= self.canvas.create_oval(x-1.5, y-1.5, x+1.5, y+1.5, fill="white", outline="white", tags="black")
            self.black_points.append((x, y))  # Store points as (x, y) tuples

        end_time= time.perf_counter()
        elapsed_time= (end_time- start_time) * 1000
        self.output_box.insert(tk.END, f"Time to generate points: {elapsed_time:.6f} ms\n")

    def drag(self, event):
        widget = event.widget
        x, y = event.x, event.y
        widget.coords(tk.CURRENT, x-1.5, y-1.5, x+1.5, y+1.5)

    def closest_pair_divide_conquer(self, points):
        # Base case: Use brute-force for small datasets
        if len(points)<= 3:
            return self.closest_pair_brute_force(points)

        mid =len(points) // 2
        mid_x =points[mid][0]

        left_half= points[:mid]
        right_half= points[mid:]

        left_pair =self.closest_pair_divide_conquer(left_half)
        right_pair=self.closest_pair_divide_conquer(right_half)

        if left_pair[0] <right_pair[0]:
            min_pair=left_pair
        else:
            min_pair =right_pair

        strip = [point for point in points if abs(point[0] - mid_x) < min_pair[0]]
        strip_pair = self.closest_pair_strip(strip, min_pair[0])

        if strip_pair[0] <min_pair[0]:
            min_pair = strip_pair

        return min_pair

    def closest_pair_brute_force(self, points):
        min_dist =float("inf")
        min_pair= None

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = self.distance(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
                    min_pair = (points[i], points[j])

        return (min_dist, min_pair)

    def closest_pair_strip(self, strip, min_dist):
        min_dist_strip = min_dist
        min_pair_strip = None

        strip.sort(key=lambda point: point[1])

        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1]-strip[i][1])>= min_dist_strip:
                    break
                dist = self.distance(strip[i], strip[j])
                if dist<min_dist_strip:
                    min_dist_strip = dist
                    min_pair_strip = (strip[i], strip[j])

        return (min_dist_strip, min_pair_strip)

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def find_and_draw_closest_pair(self):
        start_time =time.perf_counter()
        self.canvas.delete("line")
        for circle in self.highlighted_circles:
            self.canvas.delete(circle)

        sorted_points=sorted(self.black_points, key=lambda point: point[0])

        min_dist, closest_pair= self.closest_pair_divide_conquer(sorted_points)

        if closest_pair:
            for point in closest_pair:
                self.canvas.create_oval(point[0]-1.5 , point[1]-1.5, point[0]+1.5, point[1]+1.5 , fill="red",outline="red")

            r = 10
            for point in closest_pair:
                circle = self.canvas.create_oval(point[0]-r, point[1]-r, point[0]+r, point[1]+r, outline="red", width=2, tags="highlight")
                self.highlighted_circles.append(circle)

            self.canvas.create_line(closest_pair[0][0], closest_pair[0][1],
                                    closest_pair[1][0], closest_pair[1][1],
                                    fill="cyan", width=2, tags= "line")

        end_time =time.perf_counter()
        elapsed_time =(end_time - start_time) * 1000

        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"Point 1 (x, y): ({closest_pair[0][0]:.2f}, {closest_pair[0][1]:.2f})\n")
        self.output_box.insert(tk.END, f"Point 2 (x, y): ({closest_pair[1][0]:.2f}, {closest_pair[1][1]:.2f})\n")
        self.output_box.insert(tk.END, f"Distance: {min_dist:.2f}\n")
        self.output_box.insert(tk.END, f"Time to find closest pair: {elapsed_time:.6f} ms\n")

    def set_number_of_black_points(self):
        try:
            num_points= int(self.entry.get())
            if num_points<= 0:
                raise ValueError("Number of points must be positive.")
            self.create_points(num_points)
        except ValueError as e:
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, f"Invalid input: {e}")

    def reset_canvas(self):
        self.create_points(10)
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, "Coordinates of the closest pair of points will appear here.\n")

        for circle in self.highlighted_circles:
            self.canvas.delete(circle)
        self.highlighted_circles.clear()

if __name__ == "__main__":
    root=tk.Tk()
    app=ClosestPairNightModeApp(root)
    root.mainloop()
