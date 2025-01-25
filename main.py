import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'test_sample.csv'
data = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip', lineterminator='\n')


def perform_eda(data):
    """
    Perform Exploratory Data Analysis on the dataset

    Args:
        data (pd.DataFrame): Input DataFrame

    Returns:
        dict: Key insights from the analysis
    """
    # 1. Basic Dataset Information
    print("Dataset Basic Information:")
    print(f"Total Records: {len(data)}")
    print(f"Columns: {list(data.columns)}\n")

    # 2. Data Types and Missing Values
    print("Data Types and Missing Values:")
    print(data.info())
    print("\nMissing Values:")
    print(data.isnull().sum())

    # 3. Statistical Summary
    print("\nStatistical Summary of Numeric Columns:")
    numeric_columns = ['likes_count', 'comments_count', 'views_count']
    print(data[numeric_columns].describe())

    # 4. Platform Distribution
    platform_distribution = data['platform'].value_counts(normalize=True) * 100
    print("\nPlatform Distribution:")
    print(platform_distribution)

    # 5. Time-based Analysis
    data['created_time'] = pd.to_datetime(data['created_time'])
    print("\nTime Range of Data:")
    print(f"Earliest Time: {data['created_time'].min()}")
    print(f"Latest Time: {data['created_time'].max()}")

    # 6. Correlation Analysis
    correlation_matrix = data[numeric_columns].corr()

    # 7. Visualizations
    plt.figure(figsize=(15, 10))

    # Platform Distribution
    plt.subplot(2, 2, 1)
    data['platform'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Platform Distribution')

    # Engagement Distribution
    plt.subplot(2, 2, 2)
    sns.boxplot(data=data[numeric_columns])
    plt.title('Engagement Metrics Distribution')
    plt.xticks(rotation=45)

    # Correlation Heatmap
    plt.subplot(2, 2, 3)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Between Engagement Metrics')

    # Time Series of Posts
    plt.subplot(2, 2, 4)
    data.groupby(pd.Grouper(key='created_time', freq='D')).size().plot()
    plt.title('Daily Number of Posts')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')

    plt.tight_layout()
    plt.savefig('eda_visualization.png')
    plt.close()

    # 8. Advanced Insights
    insights = {
        'total_records': len(data),
        'unique_platforms': data['platform'].nunique(),
        'total_likes': data['likes_count'].sum(),
        'total_comments': data['comments_count'].sum(),
        'total_views': data['views_count'].sum(),
        'avg_likes_per_post': data['likes_count'].mean(),
        'avg_comments_per_post': data['comments_count'].mean(),
        'avg_views_per_post': data['views_count'].mean(),
        'most_common_platform': data['platform'].mode()[0],
        'max_engagement_post': data.loc[data['likes_count'].idxmax()]['platform']
    }

    # Print Insights
    print("\nKey Insights:")
    for key, value in insights.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    return insights


# Run the analysis
analysis_results = perform_eda(data)
