import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function PowerballChart() {
	const chartRef = useRef(null);
	const chartInstance = useRef(null);

	useEffect(() => {
		if (chartInstance.current) {
			chartInstance.current.destroy();
		}

		// Sample data - in a real implementation, this would come from the Python analysis
		const sampleData = {
			regularNumbers: [2, 5, 8, 12, 15, 18, 23, 27, 31, 35, 42, 47, 51, 55, 59, 63, 67],
			frequencies: [45, 52, 38, 61, 49, 43, 55, 41, 47, 39, 53, 44, 48, 42, 46, 40, 51],
			powerballs: [3, 7, 11, 15, 19, 23],
			powerballFreq: [28, 32, 25, 31, 29, 27]
		};

		const ctx = chartRef.current.getContext('2d');

		chartInstance.current = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: sampleData.regularNumbers,
				datasets: [{
					label: 'Regular Numbers Frequency',
					data: sampleData.frequencies,
					backgroundColor: 'rgba(59, 130, 246, 0.8)',
					borderColor: 'rgba(59, 130, 246, 1)',
					borderWidth: 1
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					title: {
						display: true,
						text: 'Sample Powerball Number Frequency Analysis',
						font: {
							size: 16
						}
					},
					legend: {
						display: true,
						position: 'top'
					}
				},
				scales: {
					y: {
						beginAtZero: true,
						title: {
							display: true,
							text: 'Frequency'
						}
					},
					x: {
						title: {
							display: true,
							text: 'Numbers'
						}
					}
				}
			}
		});

		return () => {
			if (chartInstance.current) {
				chartInstance.current.destroy();
			}
		};
	}, []);

	return (
		<div className="w-full h-96">
			<canvas ref={chartRef}></canvas>
			<p className="text-sm text-gray-600 mt-4 text-center">
				This is a sample visualization. Use the Powerball Analysis Tool to generate real data visualizations.
			</p>
		</div>
	);
}
