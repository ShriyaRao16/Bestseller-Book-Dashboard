import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("bestsellers with categories.csv")

# Clean & rename columns
df.drop_duplicates(inplace=True)
df.rename(columns={
    "Name": "Title",
    "Year": "Publication Year",
    "User Rating": "Rating"
}, inplace=True)
df["Price"] = df["Price"].astype(float)

# Sidebar filters
st.sidebar.header("Filters")

# Search bar
search_term = st.sidebar.text_input("Search by title", "")

# Filter by year
years = sorted(df["Publication Year"].unique())
year_filter = st.sidebar.multiselect("Filter by year", years, default=years)

# Filter by genre
genres = sorted(df["Genre"].unique())
genre_filter = st.sidebar.multiselect("Filter by genre", genres, default=genres)

# Apply filters
filtered_df = df[
    df["Publication Year"].isin(year_filter) &
    df["Genre"].isin(genre_filter) &
    df["Title"].str.contains(search_term, case=False, na=False)
]

# Main title
st.title("📚 Bestseller Books Dashboard")

# Show data
st.write(f"Showing {len(filtered_df)} books after applying filters.")
st.dataframe(filtered_df)

# Top authors
author_counts = filtered_df["Author"].value_counts()
st.subheader("🏆 Top Authors")
st.bar_chart(author_counts.head(10))

# Average rating by genre
av_rating_by_genre = filtered_df.groupby("Genre")["Rating"].mean()
st.subheader("⭐ Average Rating by Genre")
st.bar_chart(av_rating_by_genre)

# Scatter plot: Price vs Rating
st.subheader("💲 Price vs Rating")
fig, ax = plt.subplots()
ax.scatter(filtered_df["Price"], filtered_df["Rating"], alpha=0.5)
ax.set_xlabel("Price")
ax.set_ylabel("Rating")
st.pyplot(fig)

# Download buttons
st.subheader("⬇ Download Data")
st.download_button(
    label="Download Top Authors CSV",
    data=author_counts.to_csv().encode("utf-8"),
    file_name="top_authors.csv",
    mime="text/csv"
)
st.download_button(
    label="Download Avg Rating by Genre CSV",
    data=av_rating_by_genre.to_csv().encode("utf-8"),
    file_name="avg_rating_by_genre.csv",
    mime="text/csv"
)

