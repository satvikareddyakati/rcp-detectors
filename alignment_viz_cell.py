# ILI Data Alignment Visualization
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def create_ili_alignment_diagram(pair_name="2007_to_2015"):
    """
    Create an interactive ILI alignment diagram showing how features align across runs.
    Similar to the diagram in the problem statement.
    """
    
    # Determine which datasets to use
    if pair_name == "2007_to_2015":
        src_year = "2007"
        dst_year = "2015"
        matched_df = matches_2007_2015.copy()
    else:  # 2015_to_2022
        src_year = "2015"
        dst_year = "2022"
        matched_df = matches_2015_2022.copy()
    
    # Sample some representative features for visualization (max 10-15 for clarity)
    if len(matched_df) > 15:
        # Get a mix of different categories
        sample_matched = matched_df.groupby('category', group_keys=False).apply(
            lambda x: x.sample(min(5, len(x)), random_state=42)
        ).reset_index(drop=True)[:15]
    else:
        sample_matched = matched_df.copy()
    
    # Create figure
    fig = go.Figure()
    
    # Pipeline baseline positions (y-coordinates)
    y_baseline = 2
    y_run1 = y_baseline
    y_run2 = y_baseline - 1.5
    
    # Get distance ranges
    src_distances = sample_matched['src_distance_m'].values
    dst_distances = sample_matched['dst_distance_m_aligned'].values
    
    min_dist = min(src_distances.min(), dst_distances.min()) - 1000
    max_dist = max(src_distances.max(), dst_distances.max()) + 1000
    
    # Draw pipelines (horizontal lines)
    fig.add_trace(go.Scatter(
        x=[min_dist, max_dist], y=[y_run1, y_run1],
        mode='lines',
        line=dict(color='black', width=8),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=[min_dist, max_dist], y=[y_run2, y_run2],
        mode='lines',
        line=dict(color='black', width=8),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add run labels
    fig.add_annotation(
        x=min_dist - 500, y=y_run1,
        text=f"<b>ILI Run<br>{src_year}</b>",
        showarrow=False,
        xanchor='right',
        font=dict(size=12, color='#2c3e50')
    )
    
    fig.add_annotation(
        x=min_dist - 500, y=y_run2,
        text=f"<b>ILI Run<br>{dst_year}</b>",
        showarrow=False,
        xanchor='right',
        font=dict(size=12, color='#2c3e50')
    )
    
    # Color mapping for categories
    category_colors = {
        'matched': '#27ae60',      # green
        'uncertain': '#f39c12',    # orange
        'new': '#e74c3c',          # red
        'disappeared': '#95a5a6'   # gray
    }
    
    # Symbol mapping for feature types
    type_symbols = {
        'Anomaly': 'circle',
        'Bend': 'diamond',
        'Valve': 'star',
        'Tee': 'hexagon',
        'Girth Weld': 'square',
        'unknown': 'x'
    }
    
    # Plot features on both runs
    for idx, row in sample_matched.iterrows():
        src_dist = row['src_distance_m']
        dst_dist = row['dst_distance_m_aligned']
        category = row.get('category', 'matched')
        feature_type = row.get('type_norm', 'unknown')
        
        color = category_colors.get(category, '#3498db')
        symbol = type_symbols.get(feature_type, 'circle')
        
        # Feature on source run
        fig.add_trace(go.Scatter(
            x=[src_dist], y=[y_run1],
            mode='markers',
            marker=dict(
                size=12,
                color=color,
                symbol=symbol,
                line=dict(color='white', width=1)
            ),
            name=feature_type,
            showlegend=False,
            hovertemplate=(
                f"<b>{src_year} Run</b><br>" +
                f"Type: {feature_type}<br>" +
                f"Distance: {src_dist:.0f}m<br>" +
                f"ID: {row.get('src_id', 'N/A')}<br>" +
                f"Category: {category}<br>" +
                "<extra></extra>"
            )
        ))
        
        # Feature on destination run
        fig.add_trace(go.Scatter(
            x=[dst_dist], y=[y_run2],
            mode='markers',
            marker=dict(
                size=12,
                color=color,
                symbol=symbol,
                line=dict(color='white', width=1)
            ),
            showlegend=False,
            hovertemplate=(
                f"<b>{dst_year} Run</b><br>" +
                f"Type: {feature_type}<br>" +
                f"Aligned Distance: {dst_dist:.0f}m<br>" +
                f"ID: {row.get('dst_id', 'N/A')}<br>" +
                f"Category: {category}<br>" +
                f"Confidence: {row.get('confidence', 0):.2f}<br>" +
                "<extra></extra>"
            )
        ))
        
        # Draw alignment line (dashed red line connecting matched features)
        if category == 'matched':
            fig.add_trace(go.Scatter(
                x=[src_dist, dst_dist],
                y=[y_run1 - 0.15, y_run2 + 0.15],
                mode='lines',
                line=dict(color='#e74c3c', width=1, dash='dash'),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Add legend manually
    legend_items = [
        ('Matched', category_colors['matched']),
        ('Uncertain', category_colors['uncertain']),
        ('New', category_colors['new']),
    ]
    
    for i, (label, color) in enumerate(legend_items):
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color=color, line=dict(color='white', width=1)),
            name=label,
            showlegend=True
        ))
    
    # Add feature type symbols to legend
    common_types = ['Anomaly', 'Bend', 'Valve', 'Girth Weld']
    for ftype in common_types:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color='gray', symbol=type_symbols.get(ftype, 'circle')),
            name=ftype,
            showlegend=True
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>ILI Data Alignment: {src_year} → {dst_year}</b><br>" +
                 "<sub>Same pipeline features appear at different locations in each ILI run</sub>",
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        xaxis=dict(
            title="Distance along pipeline (m)",
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[y_run2 - 0.5, y_run1 + 0.5]
        ),
        height=500,
        width=1400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="gray",
            borderwidth=1
        )
    )
    
    return fig

# Generate for both pairs
print("Generating ILI alignment diagrams...")

try:
    # 2007 to 2015 alignment
    fig_07_15 = create_ili_alignment_diagram("2007_to_2015")
    alignment_path_07_15 = os.path.join(output_dir, "ili_alignment_2007_to_2015.html")
    pio.write_html(fig_07_15, file=alignment_path_07_15, auto_open=False, include_plotlyjs="cdn")
    print(f"Saved: {alignment_path_07_15}")
    fig_07_15.show()
    
    # 2015 to 2022 alignment
    fig_15_22 = create_ili_alignment_diagram("2015_to_2022")
    alignment_path_15_22 = os.path.join(output_dir, "ili_alignment_2015_to_2022.html")
    pio.write_html(fig_15_22, file=alignment_path_15_22, auto_open=False, include_plotlyjs="cdn")
    print(f"Saved: {alignment_path_15_22}")
    fig_15_22.show()
    
except Exception as e:
    print(f"Error generating alignment diagrams: {e}")
    import traceback
    traceback.print_exc()
