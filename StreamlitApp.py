# Nicolas Moy
# DSCI 551 Semester Project

import streamlit as st
import os
import tempfile
from Project import load_csv, dataFrame


st.set_page_config(page_title="NBA Data Analysis - DSCI 551 Project", layout="wide")

col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    st.image("warriors_logo.png")
# Title and pictures
with col2:
    st.markdown('<h1 class="main-header">🏀 NBA Data Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Nicolas Moy DSCI 551 Semester Project - Solo Option**")
st.markdown("---")
with col3:
    st.image("usc_logo.png", width=400)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #1E90FF;
        text-align: center;
        padding: 20px 0;
        font-size: 48px;
        font-weight: bold;
        border-bottom: 3px solid #FF6347;
        margin-bottom: 30px;
    }
    .section-header {
        color: #FF6347;
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)



# Initialize session state for dataframes
if 'player_df' not in st.session_state:
    st.session_state.player_df = None
if 'warriors_df' not in st.session_state:
    st.session_state.warriors_df = None

# Sidebar for file uploads
st.sidebar.title("📁 Data Upload")
st.sidebar.write("Upload your CSV files to begin analysis")

# File uploaders
player_file = st.sidebar.file_uploader("Upload Player Data CSV", type=['csv'], key="player_upload")
warriors_file = st.sidebar.file_uploader("Upload Warriors Stats CSV", type=['csv'], key="warriors_upload")

# Process uploaded files
if player_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        content = player_file.read().decode('utf-8')
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Load the CSV using our custom function
        data, columns = load_csv(tmp_path)
        st.session_state.player_df = dataFrame(data, columns)
        st.sidebar.success("✅ Player data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading player data: {str(e)}")
    finally:
        # Clean up temp file
        os.unlink(tmp_path)

if warriors_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        content = warriors_file.read().decode('utf-8')
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Load the CSV using our custom function
        data, columns = load_csv(tmp_path)
        st.session_state.warriors_df = dataFrame(data, columns)
        st.sidebar.success("✅ Warriors data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading warriors data: {str(e)}")
    finally:
        # Clean up temp file
        os.unlink(tmp_path)

# //////////////////////  Main content area  ///////////////////////////////////////////////
if st.session_state.player_df is None and st.session_state.warriors_df is None:
    # Instructions when no data is loaded
    st.info("👈 Please upload CSV files using the sidebar to begin")
    st.markdown("###  Instructions:")
    st.markdown("""
    1. Use the sidebar to upload your CSV files
    2. Upload the **Player Data CSV** (containing player statistics)
    3. Upload the **Warriors Stats CSV** (containing team-specific data)
    4. Once loaded, you can explore various SQL-like operations
    """)
    
    st.markdown("###  Available Operations:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **SELECT** - Project specific columns
        - **WHERE** - Filter rows by conditions
        - **GROUP BY** - Group data by attributes
        """)
    with col2:
        st.markdown("""
        - **Aggregations** - SUM, AVG, MAX, MIN, COUNT
        - **JOIN** - Combine multiple tables
        - **Custom Queries** - Build complex operations
        """)
else:
    # Display loaded data information
    st.markdown('<h2 class="section-header">📊 Loaded Datasets</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.player_df:
            st.metric("Player Dataset", 
                     f"{st.session_state.player_df.shape[0]} rows × {st.session_state.player_df.shape[1]} columns")
        else:
            st.info("Player data not loaded")
    
    with col2:
        if st.session_state.warriors_df:
            st.metric("Warriors Dataset", 
                     f"{st.session_state.warriors_df.shape[0]} rows × {st.session_state.warriors_df.shape[1]} columns")
        else:
            st.info("Warriors data not loaded")
    
    st.markdown("---")
    
    # Operations tabs
    if st.session_state.warriors_df:
        operation = st.selectbox(
            "Select Operation to Demonstrate:",
            ["Data Preview", "SELECT (Projection)", "WHERE (Filtering)", 
             "Aggregation Functions", "JOIN Operations"]
        )
        
        # Using warriors stats for dataframe operations
        df = st.session_state.warriors_df
        df2 = st.session_state.player_df
        
        if operation == "Data Preview":
            st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
            st.write("First 10 rows of Warriors data:")
            
            # Create preview of warriors data
            preview_data = {}
            num_rows = min(10, df.shape[0])
            for col in df.column_names[:9]:  # Show first 8 columns
                preview_data[col] = [df.data[col][i] for i in range(num_rows)]
            st.dataframe(preview_data)
            
            # Show column info
            with st.expander("View Column Names"):
                st.write(df.column_names)

            st.write("First 10 rows of Player Data:")
            
            # Create preview of Player data
            preview_data2 = {}
            num_rows2 = min(10, df2.shape[0])
            for col in df2.column_names[:8]:  # Show first 8 columns
                preview_data2[col] = [df2.data[col][i] for i in range(num_rows2)]
            st.dataframe(preview_data2)

            # Show column info
            with st.expander("View Column Names"):
                st.write(df2.column_names)
        
        elif operation == "SELECT (Projection)":
            st.markdown('<h2 class="section-header">SELECT Operation - Column Projection</h2>', unsafe_allow_html=True)
            
            selected_columns = st.multiselect(
                "Choose columns to select:",
                df.column_names,
                default=df.column_names[:3] if len(df.column_names) >= 3 else df.column_names
            )
            
            if st.button("Execute SELECT", key="select_btn"):
                if selected_columns:
                    result = df.select(selected_columns)
                    st.code(f"df.select({selected_columns})", language="python")
                    
                    # Display results
                    st.success(f"✅ Selected {len(selected_columns)} columns")
                    result_data = {}
                    num_rows = min(10, result.shape[0])
                    for col in selected_columns:
                        result_data[col] = [result.data[col][i] for i in range(num_rows)]
                    st.dataframe(result_data)
                else:
                    st.warning("Please select at least one column")
        
        elif operation == "WHERE (Filtering)":
            st.markdown('<h2 class="section-header">WHERE Operation - Row Filtering</h2>', unsafe_allow_html=True)
            
            filter_mode = st.radio("Filter Mode:", ["Basic Filter", "Condition Filter"])
            
            if filter_mode == "Basic Filter":
                filter_col = st.selectbox("Select column to filter:", df.column_names)
                
                #getting value to filter
                filter_value = st.text_input("Enter value to filter by:")
        
                if st.button("Apply Filter", key="where_btn"):
                    if filter_value:
                        # Try to convert to appropriate type
                        try:
                            # Try to convert to number if possible
                            if '.' in filter_value:
                                typed_value = float(filter_value)
                            elif filter_value.isdigit() or (filter_value.startswith('-') and filter_value[1:].isdigit()):
                                typed_value = int(filter_value)
                            elif filter_value.lower() in ['true', 'false']:
                                typed_value = filter_value.lower() == 'true'
                            else:
                                typed_value = filter_value
                        except:
                            typed_value = filter_value
                        
                        result = df.where({filter_col: typed_value})
                        st.code(f"df.where({{'{filter_col}': {typed_value}}})", language="python")
                        st.success(f"✅ Found {result.shape[0]} matching rows")
                        
                        if result.shape[0] > 0:
                            # Show results
                            result_data = {}
                            num_rows = min(10, result.shape[0])
                            for col in result.column_names[:6]:
                                result_data[col] = [result.data[col][i] for i in range(num_rows)]
                            st.dataframe(result_data)
                    else:
                        st.warning("Please enter a value to filter by")
            else:
                st.write("Custom condition example: Filter by numeric comparison")
                numeric_cols = [col for col in df.column_names if any(isinstance(df.data[col][i], (int, float)) 
                                                                      for i in range(min(10, df.shape[0])) 
                                                                      if df.data[col][i] is not None)]
                if numeric_cols:
                    col_choice = st.selectbox("Select numeric column:", numeric_cols)
                    threshold = st.number_input("Enter threshold value:", value=0)
                    comparison = st.selectbox("Comparison:", [">", "<", ">=", "<=", "=="])
                    
                    if st.button("Apply Custom Filter"):
                        if comparison == ">":
                            result = df.where(lambda row: row[col_choice] > threshold if row[col_choice] else False)
                        elif comparison == "<":
                            result = df.where(lambda row: row[col_choice] < threshold if row[col_choice] else False)
                        elif comparison == ">=":
                            result = df.where(lambda row: row[col_choice] >= threshold if row[col_choice] else False)
                        elif comparison == "<=":
                            result = df.where(lambda row: row[col_choice] <= threshold if row[col_choice] else False)
                        else:
                            result = df.where(lambda row: row[col_choice] == threshold if row[col_choice] else False)
                        
                        st.code(f"df.where(lambda row: row['{col_choice}'] {comparison} {threshold})", language="python")
                        st.success(f"✅ Found {result.shape[0]} matching rows")

                        if result.shape[0] > 0:
                            # Show results
                            result_data = {}
                            num_rows = min(10, result.shape[0])
                            for col in result.column_names[:6]:
                                result_data[col] = [result.data[col][i] for i in range(num_rows)]
                            st.dataframe(result_data)
                        else:
                            st.info("No rows meet ccndition")
        
        elif operation == "Aggregation Functions":
            st.markdown('<h2 class="section-header">Aggregation Functions</h2>', unsafe_allow_html=True)
            
            agg_function = st.selectbox("Select Aggregation:", ["COUNT", "SUM", "AVG", "MAX", "MIN"])
            group_by_col = st.selectbox("Group By Column:", df.column_names)
            
            if agg_function != "COUNT":
                # Need a column to aggregate
                numeric_cols = [col for col in df.column_names if col != group_by_col and 
                               any(isinstance(df.data[col][i], (int, float)) 
                                  for i in range(min(10, df.shape[0])) if df.data[col][i] is not None)]
                if numeric_cols:
                    agg_col = st.selectbox("Column to Aggregate:", numeric_cols)
                else:
                    st.error("No numeric columns available for aggregation")
                    agg_col = None
            
            if st.button("Execute Aggregation", key="agg_btn"):
                if agg_function == "COUNT":
                    result = df.count(group_by_col)
                    st.code(f"df.count('{group_by_col}')", language="python")
                elif agg_col:
                    if agg_function == "SUM":
                        result = df.sum(group_by_col, agg_col)
                        st.code(f"df.sum('{group_by_col}', '{agg_col}')", language="python")
                    elif agg_function == "AVG":
                        result = df.avg(group_by_col, agg_col)
                        st.code(f"df.avg('{group_by_col}', '{agg_col}')", language="python")
                    elif agg_function == "MAX":
                        result = df.max(group_by_col, agg_col)
                        st.code(f"df.max('{group_by_col}', '{agg_col}')", language="python")
                    elif agg_function == "MIN":
                        result = df.min(group_by_col, agg_col)
                        st.code(f"df.min('{group_by_col}', '{agg_col}')", language="python")
                
                # Display results
                if 'result' in locals():
                    st.success(f"✅ Aggregation complete - {result.shape[0]} groups")
                    result_data = {}
                    for col in result.column_names:
                        result_data[col] = result.data[col]
                    st.dataframe(result_data)
        
        elif operation == "JOIN Operations":
            st.markdown('<h2 class="section-header">JOIN Operations</h2>', unsafe_allow_html=True)
            
            if st.session_state.player_df:  # Need player data for join
                st.write("Join Warriors data with Player data")
                
                # Let user select join keys
                left_key = st.selectbox("Warriors table key:", df.column_names)
                right_key = st.selectbox("Player table key:", st.session_state.player_df.column_names)
                
                if st.button("Execute JOIN", key="join_btn"):
                    # Perform the join - warriors JOIN players
                    result = df.join(st.session_state.player_df, left_key, right_key)
                    st.code(f"warriors.join(players, '{left_key}', '{right_key}')", language="python")
                    st.success(f"✅ Join complete - {result.shape[0]} matched rows")
                    
                    # Show sample of joined data with columns from BOTH tables
                    if result.shape[0] > 0:
                        columns_to_show = []
                
                        # Add some warriors csv columns
                        warriors_cols = ['player_id', 'games_played', 'points_per_game', 'minutes_per_game', 'salary']
                        for col in warriors_cols:
                            if col in result.column_names:
                                columns_to_show.append(col)
                        
                        # Add some player csv columns
                        player_cols = ['full_name', 'first_name', 'last_name', 'is_active']
                        for col in player_cols:
                            if col in result.column_names:
                                columns_to_show.append(col)
                        
                        # Display the data
                        st.write("**Joined Data:**")
                        result_data = {}
                        num_rows = min(10, result.shape[0])
                        for col in columns_to_show[:10]:  # Limit to 10 columns for display
                            if col in result.data:
                                result_data[col] = [result.data[col][i] for i in range(num_rows)]
                        
                        st.dataframe(result_data)
                        
                        #  Show columns of joined table
                        with st.expander("View all columns in joined result"):
                            st.write("**All columns after join:**")
                            st.write(result.column_names)
                    else:
                        st.warning("No matching rows found in join operation")
            else:
                st.warning("Please upload Player data to demonstrate JOIN operations")

# Footer
st.markdown("---")
