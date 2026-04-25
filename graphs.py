import matplotlib.pyplot as plt
import numpy as np

def plot_system_metrics(metrics):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('System Performance Metrics', fontsize=14, fontweight='bold')
    
    labels = ['CPU', 'RAM', 'Disk']
    values = [metrics['cpu'], metrics['ram'], metrics['disk']]
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    axes[0, 0].bar(labels, values, color=colors)
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].set_title('Usage Percentage')
    axes[0, 0].set_ylabel('Percentage (%)')
    
    axes[0, 1].pie([100-metrics['cpu'], metrics['cpu']], 
                   labels=['Free', 'Used'],
                   colors=['#bdc3c7', '#3498db'],
                   autopct='%1.1f%%')
    axes[0, 1].set_title('CPU Usage')
    
    io_labels = ['Read Speed', 'Write Speed']
    io_values = [metrics['read_speed'], metrics['write_speed']]
    axes[1, 0].barh(io_labels, io_values, color=['#9b59b6', '#f39c12'])
    axes[1, 0].set_xlabel('MB/s')
    axes[1, 0].set_title('Disk I/O Speed')
    
    sizes = [100-metrics['ram'], metrics['ram']]
    axes[1, 1].pie(sizes, 
                   labels=['Free', 'Used'],
                   colors=['#bdc3c7', '#2ecc71'],
                   autopct='%1.1f%%')
    axes[1, 1].set_title('RAM Usage')
    
    plt.tight_layout()
    plt.savefig('system_metrics.png', dpi=100, bbox_inches='tight')
    plt.show()

def plot_scheduler_comparison(results, best_algorithm):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algorithms = list(results.keys())
    seeks = [results[alg]['total'] for alg in algorithms]
    colors = ['#3498db' if alg != best_algorithm else '#27ae60' for alg in algorithms]
    
    bars = ax.bar(algorithms, seeks, color=colors, edgecolor='black')
    
    for bar, seek in zip(bars, seeks):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                str(int(seek)), ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Scheduling Algorithm', fontsize=12)
    ax.set_ylabel('Total Seek Operations', fontsize=12)
    ax.set_title(f'Disk Scheduling Comparison (Best: {best_algorithm})', fontsize=14, fontweight='bold')
    ax.axhline(y=min(seeks), color='r', linestyle='--', alpha=0.5, label=f'Minimum: {min(seeks)}')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('scheduler_comparison.png', dpi=100, bbox_inches='tight')
    plt.show()

def plot_health_gauge(health_status):
    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})
    
    status_map = {'Healthy': 0, 'Warning': 1, 'Critical': 2}
    status_colors = {'Healthy': '#27ae60', 'Warning': '#f39c12', 'Critical': '#e74c3c'}
    
    theta = np.linspace(0, np.pi, 100)
    r = np.ones_like(theta)
    
    colors = ['#27ae60', '#f39c12', '#e74c3c']
    for i, color in enumerate(colors):
        ax.fill_between(theta[i*33:(i+1)*33], 0, r[i*33:(i+1)*33], 
                        color=color, alpha=0.3)
    
    idx = status_map[health_status]
    ax.scatter([(idx + 0.5) * np.pi / 3], [1], s=200, color=status_colors[health_status], 
               edgecolor='black', linewidth=2, zorder=5)
    
    ax.set_xticks([np.pi/6, np.pi/2, 5*np.pi/6])
    ax.set_xticklabels(['Healthy', 'Warning', 'Critical'])
    ax.set_ylim(0, 1.5)
    ax.set_title(f'System Health: {health_status}', fontsize=14, fontweight='bold', pad=20)
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('health_gauge.png', dpi=100, bbox_inches='tight')
    plt.show()