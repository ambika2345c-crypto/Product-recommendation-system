import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('ai_project.csv')
# Convert to numeric properly
data['Average Rating'] = pd.to_numeric(data['Average Rating'], errors='coerce')
data['Items Purchased'] = pd.to_numeric(data['Items Purchased'], errors='coerce')
data['Satisfaction Level'] = pd.to_numeric(data['Satisfaction Level'], errors='coerce')
data = data.fillna(0)


data['rating'] = (
        data['Average Rating'] * 0.4 +
        data['Total Spend'] * 0.0001 +
        data['Items Purchased'] * 0.2 +
        data['Satisfaction Level'] * 0.3
)

data['product'] = data['Membership Type']

user_item = data.pivot_table(
    index='Customer ID',
    columns='product',
    values='rating'
).fillna(0)

similarity = cosine_similarity(user_item)

sim_df = pd.DataFrame(similarity,
                      index=user_item.index,
                      columns=user_item.index)


def recommend(user_id):
    user_id = int(user_id)

    if user_id not in user_item.index:
        return ["❌ User not found in system"]

    similar_users = sim_df[user_id].sort_values(ascending=False)[1:]
    top_user = similar_users.index[0]

    recommendations = user_item.loc[top_user].sort_values(ascending=False)

    top_products = list(recommendations.head(3).index)

    # 👉 BEAUTIFUL OUTPUT FORMAT
    output = [
        f"🎯 Personalized Recommendations for User {user_id}",
        "--------------------------------------------------",
        f"✔ {top_products[0]} (Highly matched preference)",
        f"✔ {top_products[1]} (Based on similar users)",
        f"✔ {top_products[2]} (Behavior-based suggestion)",
        "--------------------------------------------------",
        "💡 Model: Collaborative Filtering + Cosine Similarity"
    ]

    return output



print(user_item.index[:10])
