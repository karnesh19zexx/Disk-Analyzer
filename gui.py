import tkinter as tk
from tkinter import ttk, messagebox
import system_monitor
import disk_scheduler
import ml_model
import database
import graphs
import random

class DiskAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Disk I/O Performance Analyzer")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        self.current_metrics = None
        self.current_results = None
        self.current_health = None
        self.current_best_algo = None
        
        self.init_database()
        self.create_widgets()
    
    def init_database(self):
        if database.init_database():
            self.db_status = True
        else:
            self.db_status = False
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg='#34495e', pady=10)
        title_frame.pack(fill='x')
        
        title = tk.Label(title_frame, text="Intelligent Disk I/O Performance Analyzer",
                        font=('Arial', 16, 'bold'), bg='#34495e', fg='white')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Using Machine Learning",
                          font=('Arial', 10), bg='#34495e', fg='#bdc3c7')
        subtitle.pack()
        
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.metrics_frame = tk.LabelFrame(self.main_frame, text="System Metrics",
                                           font=('Arial', 11, 'bold'), bg='#2c3e50', fg='white')
        self.metrics_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=5)
        
        self.metrics_labels = {}
        metrics = ['CPU Usage', 'RAM Usage', 'Disk Usage', 'Read Speed', 'Write Speed']
        for i, metric in enumerate(metrics):
            row = i // 3
            col = i % 3 if i < 3 else (i - 3) % 3
            frame = tk.Frame(self.metrics_frame, bg='#2c3e50')
            frame.grid(row=row, column=col, padx=10, pady=5)
            
            tk.Label(frame, text=f"{metric}:", font=('Arial', 10), 
                    bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=0)
            
            value_label = tk.Label(frame, text="--", font=('Arial', 10, 'bold'),
                                  bg='#2c3e50', fg='#f39c12')
            value_label.grid(row=0, column=1)
            self.metrics_labels[metric.lower().replace(' ', '_')] = value_label
        
        self.scheduler_frame = tk.LabelFrame(self.main_frame, text="Disk Scheduling Comparison",
                                            font=('Arial', 11, 'bold'), bg='#2c3e50', fg='white')
        self.scheduler_frame.grid(row=1, column=0, sticky='nsew', pady=5)
        
        self.scheduler_labels = {}
        algorithms = ['FCFS', 'SSTF', 'SCAN', 'C-SCAN']
        for i, algo in enumerate(algorithms):
            tk.Label(self.scheduler_frame, text=f"{algo}:", font=('Arial', 10),
                    bg='#2c3e50', fg='#ecf0f1').grid(row=i, column=0, sticky='w', padx=10)
            
            value_label = tk.Label(self.scheduler_frame, text="--", font=('Arial', 10),
                                  bg='#2c3e50', fg='#3498db')
            value_label.grid(row=i, column=1, padx=10)
            self.scheduler_labels[algo] = value_label
        
        self.ml_frame = tk.LabelFrame(self.main_frame, text="ML Prediction",
                                      font=('Arial', 11, 'bold'), bg='#2c3e50', fg='white')
        self.ml_frame.grid(row=1, column=1, sticky='nsew', pady=5)
        
        tk.Label(self.ml_frame, text="Health Status:", font=('Arial', 10),
                bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=0, padx=10)
        
        self.health_label = tk.Label(self.ml_frame, text="--", font=('Arial', 12, 'bold'),
                                     bg='#2c3e50', fg='#f39c12')
        self.health_label.grid(row=0, column=1, padx=10)
        
        tk.Label(self.ml_frame, text="Best Algorithm:", font=('Arial', 10),
                bg='#2c3e50', fg='#ecf0f1').grid(row=1, column=0, padx=10, pady=10)
        
        self.best_algo_label = tk.Label(self.ml_frame, text="--", font=('Arial', 11, 'bold'),
                                        bg='#2c3e50', fg='#27ae60')
        self.best_algo_label.grid(row=1, column=1, padx=10, pady=10)
        
        self.status_frame = tk.Frame(self.root, bg='#34495e')
        self.status_frame.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(self.status_frame, text="Ready", font=('Arial', 9),
                                     bg='#34495e', fg='#bdc3c7')
        self.status_label.pack(side='left', padx=10)
        
        self.db_label = tk.Label(self.status_frame, text="DB: " + ("Connected" if self.db_status else "Disconnected"),
                                 font=('Arial', 9), bg='#34495e', fg='#27ae60' if self.db_status else '#e74c3c')
        self.db_label.pack(side='right', padx=10)
        
        self.button_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        buttons = [
            ("Analyze System", self.analyze_system, '#3498db'),
            ("Compare Algorithms", self.compare_algorithms, '#9b59b6'),
            ("ML Prediction", self.ml_prediction, '#e67e22'),
            ("Show Graph", self.show_graph, '#1abc9c'),
            ("Save to Database", self.save_to_database, '#27ae60')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=command,
                           font=('Arial', 10, 'bold'), bg=color, fg='white',
                           activebackground=color, padx=15, pady=8)
            btn.grid(row=0, column=i, padx=5)
    
    def analyze_system(self):
        self.status_label.config(text="Analyzing system...")
        self.root.update()
        
        try:
            metrics = system_monitor.get_system_metrics()
            self.current_metrics = metrics
            
            self.metrics_labels['cpu_usage'].config(text=f"{metrics['cpu']}%")
            self.metrics_labels['ram_usage'].config(text=f"{metrics['ram']}%")
            self.metrics_labels['disk_usage'].config(text=f"{metrics['disk']}%")
            self.metrics_labels['read_speed'].config(text=f"{metrics['read_speed']} MB/s")
            self.metrics_labels['write_speed'].config(text=f"{metrics['write_speed']} MB/s")
            
            self.status_label.config(text="Analysis complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_label.config(text="Analysis failed")
    
    def compare_algorithms(self):
        if not self.current_metrics:
            messagebox.showwarning("Warning", "Please analyze system first!")
            return
        
        requests = [int(random.uniform(0, 200)) for _ in range(20)]
        results, best = disk_scheduler.compare_algorithms(requests, head=100)
        self.current_results = results
        self.current_best_algo = best
        
        for algo in ['FCFS', 'SSTF', 'SCAN', 'C-SCAN']:
            self.scheduler_labels[algo].config(text=f"{results[algo]['total']} seeks")
        
        self.best_algo_label.config(text=best)
        self.status_label.config(text=f"Best: {best} algorithm")
    
    def ml_prediction(self):
        if not self.current_metrics:
            messagebox.showwarning("Warning", "Please analyze system first!")
            return
        
        health = ml_model.predict_health(
            self.current_metrics['cpu'],
            self.current_metrics['ram'],
            self.current_metrics['disk']
        )
        self.current_health = health
        
        colors = {'Healthy': '#27ae60', 'Warning': '#f39c12', 'Critical': '#e74c3c'}
        self.health_label.config(text=health, fg=colors.get(health, '#f39c12'))
        self.status_label.config(text=f"Health: {health}")
    
    def show_graph(self):
        if not self.current_metrics:
            messagebox.showwarning("Warning", "Please analyze system first!")
            return
        
        graphs.plot_system_metrics(self.current_metrics)
        
        if self.current_results and self.current_best_algo:
            graphs.plot_scheduler_comparison(self.current_results, self.current_best_algo)
        
        if self.current_health:
            graphs.plot_health_gauge(self.current_health)
        
        self.status_label.config(text="Graphs displayed!")
    
    def save_to_database(self):
        if not self.current_metrics:
            messagebox.showwarning("Warning", "Please analyze system first!")
            return
        
        if not self.current_results or not self.current_health or not self.current_best_algo:
            messagebox.showwarning("Warning", "Please run all analyses first!")
            return
        
        if database.save_result(self.current_metrics, self.current_health,
                               self.current_results, self.current_best_algo):
            messagebox.showinfo("Success", "Results saved to database!")
            self.status_label.config(text="Saved to database!")
        else:
            messagebox.showerror("Error", "Failed to save to database. Check MySQL connection.")

def main():
    root = tk.Tk()
    app = DiskAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()