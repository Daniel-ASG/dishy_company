# 1. Business problem
Dishy is a fictitious company created for the purpose of this analysis. Although it does not exist in the real world, let’s imagine that Dishy is a marketplace platform for restaurants, founded in 2015. The company has grown rapidly and now has a global presence, operating in over 20 countries and serving more than 100 cities around the world. Dishy’s mission is to facilitate meetings and negotiations between customers and restaurants, making it easier for customers to discover and experience new restaurants and for restaurants to reach new customers. Dishy’s vision is to become the world’s leading platform for restaurant discovery and online reservations. Although Dishy is a fictitious company, the following analysis is based on real data (available at this [link](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv)) and provides valuable insights that could be applied to a real company with a similar business model.

The CEO was recently hired and needs to understand the business better in order to make the best strategic decisions and leverage Dishy even more, and for this, he needs an analysis to be done on the company's data and dashboards to be generated. He would like to see the following metrics:

### On Overview:
  1. **_The number of restaurants_**: This metric provides an overview of the size of the Dishy platform. It indicates how popular and attractive the platform is to the restaurants.
  2. **_In how many countries the company operates_**: This metric indicates the geographical reach of the platform. It indicates a stronge global presence and the ability to attract customers from various backgrounds.
  3. **_How many cities it serves_**: This metric indicates the reach of the platform on a more granular level. It can help identify specific geographical areas for expansion or improvement.
  4. **_How many evaluations have been performed_**: This metric indicates the level of user engagement with the platform. A larger number of reviews may suggest that users are actively using the platform and finding value in it.
  5. **_The number of different types of cuisines on the platform_**: This metric indicates the diversity of restaurants on the platform. Greater diversity can make the platform more attractive to users as it offers more options and experiences.
  6. **_The geographical distribution of all restaurants_**: This metric can help identify geographical patterns in the restaurant base of the platform. It informs geographic marketing strategies and expansion efforts.
### On the Countries View:
  1. **_Number of registered cities per country_**: This metric can help understand the geographical distribution of restaurants on the platform. This can inform expansion strategies to new cities or countries.
  2. **_Number of registered restaurants per country_**: This metric can indicate which countries have the largest presence on the platform. This can help identify potential markets for growth.
  3. **_Number of cuisines per country_**: This metric can indicate the diversity of cuisines available in each country. This can help understand culinary preferences in different regions.
  4. **_Number of evaluations per country_**: This metric can indicate the level of user engagement in different countries. Countries with a larger number of reviews may have more active users.
  5. **_Avg Number of reviews per country_**: This metric can help understand how often users in different countries leave reviews. This can indicate the level of user engagement.
  6. **_Avg score per country_**: This metric can indicate the perceived quality of restaurants in different countries. Countries with higher average scores may have higher quality restaurants.
  7. **_Countries & Price types distribution_**: This metric can help understand the price range of restaurants in different countries. This can inform pricing strategies and market segmentation.
### On the Cities View:
  1. **_Number of registered restaurants per city_**: This metric can indicate which cities have the largest presence on the platform. This can help identify potential markets for growth.
  2. **_Number of registered cuisines per city_**: This metric can indicate the diversity of cuisines available in each city. This can help understand culinary preferences in different regions.
  3. **_Average restaurants ratings per city_**: This metric can indicate the perceived quality of restaurants in different cities. Cities with higher average scores may have higher quality restaurants.
### On the Restaurants View:
  1. **_How many restaurants are delivering now_**: This metric can indicate the delivery availability of restaurants on the platform. This can be useful for users looking for delivery options.
  2. **_How many restaurants have table booking_**: This metric can indicate the table reservation availability of restaurants on the platform. This can be useful for users planning dinners or events.
  3. **_The number of restaurants that have online delivery_**: This metric can indicate the online delivery availability of restaurants on the platform. This can be useful for users who prefer the convenience of online delivery.
  4. **_The name of the most expensive dish for two restaurants_**: This metric can help identify the most expensive restaurants on the platform. This can be useful for users looking for high-quality or luxurious options.
  5. **_Average cost for two per rating_**: This metric can help understand the relationship between price and quality of restaurants. This can be useful for users trying to find the best value.
  6. **_Top 15 Restaurants (by ratings & votes)_**: This metric can help identify the most popular and highly rated restaurants on the platform. This can be useful for users looking for the best options.
  7. **_Average cost for two (US$) by cuisines_**: This metric can help understand price differences between different types of cuisines. This can inform pricing strategies and help identify price arbitrage opportunities.
  8. **_Cuisines diversity distribution_**: This metric can help understand the diversity of cuisines available on the platform. This can be useful for users looking to try new types of cuisine.

The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

# 2. Assumptions made for the analysis
  1. All currencies have been converted to the US dollar to make comparisons easier.
  2. Marketplace was the business model assumed.
  3. The 3 main business views were: Countries view, Cities view and Restaurants view.

# 3. Solution Strategy
The strategy dashboard was developed using the metrics that reflect the main business model views of the company.

# 4. Top 4 Data Insights
1. The Major Market is in **India**, with Nearly 45% of the Number of Restaurants:
    - Nearly half of Dishy's establishments are in India, its major market. India is the company's most established market, making it a key operational hub.
    - Dishy may exploit this knowledge in numerous ways. Start by offering premium advertising packages and targeted service prices to boost revenue in this critical sector. Second, using India's diverse restaurant selections, regional marketing campaigns and loyalty programs can boost user engagement and loyalty.
    - Promoting Indian foods in marketing efforts and relationships with local influencers can increase platform engagement by attracting a diverse user base. Regional advertising and promotions can boost brand awareness and usership.
    - Finally, India's large restaurant presence offers Dishy a great opportunity to enhance income, user engagement, and brand awareness. Based on localized strategies and culinary diversity, Dishy may strengthen its market leadership and reproduce it in other rising markets.

2. Restaurants that receive many reviews will often have a higher rating. It is worth investing in requesting that customers rate the service.
    - Analysis suggests that restaurants with more reviews have higher ratings. This trend implies that aggressively promoting client input might boost a restaurant's platform reputation.
    - Dishy can use this insight to boost consumer reviews. Follow-up emails, in-app notifications, and tiny reviews incentives are examples. Restaurants gain visibility and consumers by encouraging more reviews.
    - In conclusion, encouraging customers to post evaluations can enhance restaurant ratings and Dishy's engagement and quality image.

3. The market in the American continent has potential but is still very little explored.
    - Dishy has a large growth possibility in the unexplored American market, according to the analysis. Despite its potential, fewer restaurants are registered than in other regions.
    - Dishy can use this to expand in North and South America. The platform attracts new restaurants and users through targeted marketing strategies, collaborations with local restaurant chains, and specialized incentives.
    - Dishy can reach a wide, diverse consumer base and develop a strong presence in a fast-growing region by investing in the US market. This strategic approach can boost platform growth, brand awareness, and market share.
    - After exploring and investing in the Americas, Dishy can become a leader in an underexploited market.
   
4. Understanding Preferred Cuisines by Users Can Enhance Dishy's Growth Strategies.
    - Dishy must understand consumer gastronomic preferences in each region and location to improve its growth plans. Tailoring the platform's offers to local preferences helps boost user engagement and retention.
    - Dishy may use this data to identify regional favourite cuisines and change its marketing and restaurant suggestions. Dishy may grow its audience and market share by emphasizing local cuisines.
    - Identifying culinary trends can also inform expansion and cooperation initiatives. Dishy can remain ahead of the curve and provide interesting dining experiences by monitoring consumer preferences.
    - In conclusion, using user preferences for cuisines in its growth tactics helps Dishy cater to local tastes, increase user engagement, and stay competitive in a changing market.

# 5. The final product of the project
The aim of this project was to create an App that presents insights in an effective and intuitive way for the CEO. Through the strategic use of technology and data analysis, it was possible to identify lucrative business opportunities in the King County real estate market.

The app not only provides an overview of the market, but also offers insights into factors that influence real estate prices. This allows House Rocket to make informed decisions and maximize its profits.

In addition, the app demonstrates the power of data analysis and technology in transforming the real estate sector. It highlights how House Rocket is at the forefront of this transformation, using technology to improve the way we buy and sell real estate.

Ultimately, this project serves as an example of the potential of data analytics in generating actionable insights and driving business success.

To access the final result, please go to the [Streamlit dashboard link](https://daniel-asg-dishy-company.streamlit.app/).

# 6. Conclusion
The aim of this project was to create an app that presents insights effectively and intuitively for Dishy's CEO. Through the strategic use of technology and data analysis, it was possible to identify lucrative business opportunities in the restaurant market.

However, Dishy's true potential lies in its ability to adapt and grow. Our analysis has shown substantial expansion opportunities, particularly in the American continent, which remains relatively untapped. Furthermore, understanding users' culinary preferences can be a powerful strategy for driving growth. For instance, if we knew that Italian cuisine is particularly popular in a specific city, Dishy could focus on attracting more Italian restaurants to that area.

Additionally, Dishy has demonstrated an impressive commitment to quality. With an average rating of **4.127** across all reviews, it's evident that users value the experience Dishy provides. This is further exemplified when we look at individual restaurants - for example, our top-rated restaurant, **_Byg Brewski Brewing Company_**, boasts an impressive rating of **4.90** and **17394** reviews.

Furthermore, Dishy has proven to be a profitable platform for both restaurants and users. With an average cost of **US$29.59** per meal for two, restaurants on the Dishy platform are generating significant revenue.

In summary, Dishy is more than just a restaurant platform - it's a revolution in how we interact with food. With its combination of global reach, commitment to quality, and growth potential, we believe Dishy is perfectly positioned to lead this revolution. We look forward to seeing what the future holds for Dishy.

# 7. Next steps
1. Detail some analysis regarding cuisines types.
2. Deepen the analyses regarding the evaluations provided.
3. Create new filters.
4. Add new business views.
5. Develop Machine Learning Models that can help the company improve its performance.

