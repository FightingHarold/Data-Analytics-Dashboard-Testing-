"""
Real-Time Data Analytics Dashboard
"""
import json
import statistics
from datetime import datetime
from typing import List, Dict, Union
from collections import defaultdict


class DataAnalyzer:

    
    def __init__(self, data_source: List[Dict]):
        """Initialize the analyzer with a data source."""
        self.data = data_source
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def calculate_statistics(self, metric: str) -> Dict:
        """Calculate mean, median, std dev, and range for a given metric."""
        # Extract only numeric values for the specified metric
        values = []
        for d in self.data:
            if metric in d:
                value = d[metric]
                # Check if value is numeric (int or float)
                if isinstance(value, (int, float)):
                    values.append(value)
        
        if not values:
            return {"error": f"Metric '{metric}' not found or contains no numeric data"}
        
        return {
            "metric": metric,
            "count": len(values),
            "mean": round(statistics.mean(values), 2),
            "median": statistics.median(values),
            "std_dev": round(statistics.stdev(values), 2) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values)
        }
    
    def detect_anomalies(self, metric: str, threshold: float = 2.0) -> List[Dict]:
        """Detect outliers using standard deviation method."""
        # Extract only numeric values
        values = []
        for d in self.data:
            if metric in d and isinstance(d[metric], (int, float)):
                values.append(d[metric])
        
        if not values or len(values) < 2:
            return []
        
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        anomalies = []
        
        for i, val in enumerate(values):
            if abs(val - mean) > threshold * std_dev:
                anomalies.append({
                    "index": i,
                    "value": val,
                    "deviation": round(abs(val - mean) / std_dev, 2),
                    "status": " ANOMALY"
                })
        
        return anomalies
    
    def group_and_aggregate(self, group_key: str, metric: str) -> Dict:
        """Group data by category and aggregate metrics."""
        groups = defaultdict(list)
        
        for item in self.data:
            if group_key in item and metric in item and isinstance(item[metric], (int, float)):
                groups[item[group_key]].append(item[metric])
        
        result = {}
        for group, values in groups.items():
            if values:  # Only process if we have values
                result[group] = {
                    "count": len(values),
                    "total": round(sum(values), 2),
                    "average": round(sum(values) / len(values), 2),
                    "min": min(values),
                    "max": max(values)
                }
        
        return result
    
    def get_numeric_fields(self) -> List[str]:
        """Get list of all numeric fields in the dataset."""
        numeric_fields = set()
        for item in self.data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    numeric_fields.add(key)
        return sorted(list(numeric_fields))
    
    def export_report(self, metric: str, filename: str = "analytics_report.json") -> str:
        """Export complete analysis report to JSON."""
        report = {
            "generated_at": self.timestamp,
            "data_points": len(self.data),
            "analyzed_metric": metric,
            "statistics": self.calculate_statistics(metric),
            "anomalies": self.detect_anomalies(metric)
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return f" Report exported to {filename}"


# ===== DEMO =====
if __name__ == "__main__":
    # Sample sensor data (e.g., temperature readings)
    sensor_data = [
        {"timestamp": "2025-11-25 12:00", "temperature": 22.5, "humidity": 45, "sensor_id": "A1"},
        {"timestamp": "2025-11-25 12:05", "temperature": 23.1, "humidity": 46, "sensor_id": "A1"},
        {"timestamp": "2025-11-25 12:10", "temperature": 45.8, "humidity": 47, "sensor_id": "A1"},  # Anomaly
        {"timestamp": "2025-11-25 12:15", "temperature": 22.9, "humidity": 44, "sensor_id": "A1"},
        {"timestamp": "2025-11-25 12:20", "temperature": 23.3, "humidity": 45, "sensor_id": "A1"},
    ]
    
    # Initialize analyzer
    analyzer = DataAnalyzer(sensor_data)
    
    print("First Github project ready to upload\n")
    print("=" * 50)
    
    # Show available numeric fields
    print("\n AVAILABLE NUMERIC METRICS:")
    for field in analyzer.get_numeric_fields():
        print(f"  → {field}")
    
    # Display temperature statistics
    print("\nTEMPERATURE STATISTICS:")
    stats = analyzer.calculate_statistics("temperature")
    if "error" not in stats:
        for key, value in stats.items():
            print(f"  {key.upper()}: {value}")
    else:
        print(f"   {stats['error']}")
    
    # Display humidity statistics
    print("\nHUMIDITY STATISTICS:")
    humidity_stats = analyzer.calculate_statistics("humidity")
    if "error" not in humidity_stats:
        for key, value in humidity_stats.items():
            print(f"  {key.upper()}: {value}")
    
    # Detect temperature anomalies
    anomalies = analyzer.detect_anomalies("temperature", threshold=2.0)
    print(f"\n TEMPERATURE ANOMALIES DETECTED: {len(anomalies)}")
    for anomaly in anomalies:
        print(f"  → Index {anomaly['index']}: {anomaly['value']}°C (Deviation: {anomaly['deviation']}σ)")
    
    # Group by sensor
    print("\n GROUPING BY SENSOR ID:")
    grouped = analyzer.group_and_aggregate("sensor_id", "temperature")
    for sensor, data in grouped.items():
        print(f"\n  Sensor {sensor}:")
        for key, value in data.items():
            print(f"    {key}: {value}")
    
    # Export report
    print("\n" + analyzer.export_report("temperature"))
    print("=" * 50)
