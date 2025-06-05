# Echo-Chamber Analysis on Mastodon 🌐

This repository contains sample codes for the methodology described in the research paper:

📍 [Investigating Echo-Chambers in Decentralized Social Networks: A Mastodon Case Study](https://link.springer.com/chapter/10.1007/978-3-031-82431-9_26).

The scripts implement techniques to identify potential echo-chambers on the Mastodon social network by analyzing network structural properties of both original toot networks and reply networks.

## Methodology Overview

The methodology focuses on two primary network types and one influential user analysis:

1.  **Reply Network Analysis (Context Graphs):**
    *   **Context Definition:** Conversations in Mastodon, including ancestors and descendants of toots (similar to threads).
    *   **Graph Construction:** For each context, a "context graph" is built.
        *   **Nodes:** Accounts that replied (descendants) to the original toot within that context.
        *   **Edges:** A mutual (two-way) following relationship between two replier accounts.
    *   **Sentiment Analysis:** Reply texts are analyzed for sentiment (positive/negative). Context graphs are then divided into positive and negative sentiment subgraphs.
    *   **Echo-Chamber Detection:**
        *   **Clustering Coefficient:** Applied to each sentiment-based subgraph. An echo-chamber is suspected if a subgraph with nodes sharing the same sentiment has a Clustering Coefficient of **0.5 or higher**.
        *   **Inter-Subgraph Connectivity:** The absence of links between the positive and negative sentiment subgraphs within the same context is also an indicator of potential echo-chamber formation, as communities with differing views might be isolating themselves.

2.  **Original Toot Network Analysis:**
    *   **Graph Construction:** For each sociopolitical hashtag, a graph is created.
        *   **Nodes:** Accounts that posted an original toot (not a reply) using the same hashtag.
        *   **Edges:** A mutual following relationship between these accounts.
    *   **Analysis:** The Clustering Coefficient is applied to this graph to assess the likelihood of echo-chamber formation among original posters. (The paper notes these values were generally low).

3.  **Co-follower Matrix and Common Reference Metric (Influential Users):**
    *   **Influential User Identification:** The top 5 users with the highest degree (and/or betweenness centrality, as per paper) are identified from the original toot network for each hashtag.
    *   **Co-follower Matrix Construction:** For these influential users, a matrix is built by counting the number of shared followers between each pair.
    *   **Normalization:** Values are normalized using the Cosine Co-Citation formula:
        `Normalized Co-follower(A, B) = Co-followers(A, B) / sqrt(Followers(A) * Followers(B))`
    *   **Normalized Common Reference Metric:** This assesses the cumulative number of normalized shared followers among all distinct pairs of influential users:
        `Normalized Common Reference = sum(Normalized Co-follower(i, j)) / N` (where N is the number of unique pairs) (The paper notes these values were also generally low).

## Directory Structure

The codebase and generated data are organized as follows:

*   `Mastodon_Echo_Chambers/`
    *   `contexts/{HASHTAG}_context/`: Stores data related to Mastodon contexts (conversations/threads).
        *   `{CONTEXT_ID}_context.json`: Raw JSON data for a specific context, including ancestor and descendant toots.
        *   `{CONTEXT_ID}_context_repliers/`: Contains followings lists for each replier in that context.
            *   `{REPLIER_ID}_replier_followings.json`: JSON list of accounts followed by a specific replier.
    *   `followers/`: (General storage) Stores follower lists for specific users if fetched individually.
        *   `{USER_ID}_followers.json`: JSON list of followers for a given user ID.
    *   `followings/`: (General storage) Stores following lists for specific users if fetched individually.
        *   `{USER_ID}_followings.json`: JSON list of accounts a given user ID is following.
    *   `graphs/{HASHTAG}_graphs/`: Stores generated network graphs for reply networks in GEXF format.
        *   `{CONTEXT_ID}.gexf`: The graph of repliers for a specific context, where edges represent mutual followings. Nodes may be annotated with sentiment scores.
    *   `graphs/{HASHTAG}_root_graphs/`: Stores generated network graphs for original toot networks.
        *   `{HASHTAG}.gexf`: The graph of original posters for a hashtag.
    *   `hashtags/`: Contains JSON files with lists of statuses (toots) collected for specific hashtags.
        *   `{HASHTAG}.json`: List of toots for the given hashtag.
    *   `images/{HASHTAG}_images/`: Stores visualizations of the context graphs.
        *   `{CONTEXT_ID}.png`: Visualization of the full context graph of repliers.
        *   `{CONTEXT_ID}_sentiment.png`: Visualization of the positive and negative sentiment subgraphs for a context.
    *   `images/{HASHTAG}_root_images/`: Stores visualizations of the original toot graphs.
        *   `{HASHTAG}.png`: Visualization of the original toot network for the hashtag.
    *   `roots/{HASHTAG}_roots/`: Stores followings and followers lists for users who posted original toots related to a hashtag.
        *   `{USER_ID}_root_followings.json`: JSON list of accounts followed by an original poster.
        *   `{USER_ID}_root_followers.json`: JSON list of followers of an original poster (used for co-citation analysis).
    *   `texts/{HASHTAG}_texts/{CONTEXT_ID}_context/`: Stores the text content of replies.
        *   `{REPLIER_ID}.txt`: Text of replies made by a specific replier within a context, used for sentiment analysis.

## Scripts & Workflow

The analysis pipeline is executed through a series of Python scripts:

1.  **Data Collection:**
    *   `get_hashtag_statuses.py`: Fetches toots (statuses) for specified hashtags from the Mastodon API and saves them to the `hashtags/` directory.
    *   `parse_date.py`: Utility script for parsing date strings from Mastodon API responses.
    *   `count_root_replies.py`: (Optional utility) Counts replies for root statuses to understand data volume.
    *   `get_contexts.py`: For each relevant toot, fetches its full context (ancestors and descendants) and saves it to `contexts/{HASHTAG}_context/`.
    *   `get_followings.py`: Core function to retrieve the list of accounts a given user is following. Used by other scripts.
    *   `get_followers.py`: Core function to retrieve the list of followers for a given user. Used by other scripts.
    *   **For Reply Networks:**
        *   `get_followings_of_repliers.py`: Iterates through contexts and, for each replier (descendant), fetches their followings list. Saves data to `contexts/{HASHTAG}_context/{CONTEXT_ID}_context_repliers/`.
        *   `collect_replies_text.py`: Extracts the textual content of replies from the collected context data and saves them into individual text files in `texts/{HASHTAG}_texts/{CONTEXT_ID}_context/`.
    *   **For Original Toot Networks & Influential User Analysis:**
        *   `get_followings_of_roots.py`: Fetches followings lists for users who posted original toots and saves them to `roots/{HASHTAG}_roots/` as `{USER_ID}_root_followings.json`.
        *   `get_followers_of_repliers.py`: *Note: Despite its name, this script fetches followers for **root tooters (original posters)** identified in `hashtags/{HASHTAG}.json` and saves them to `roots/{HASHTAG}_roots/` as `{USER_ID}_root_followers.json`. This data is used for the co-follower analysis.*

2.  **Graph Construction:**
    *   `create_repliers_graph.py`: Constructs the "context graphs" for reply networks based on mutual following relationships between repliers. Saves graphs as GEXF files in `graphs/{HASHTAG}_graphs/`.
    *   `create_roots_graph.py`: Constructs the original toot network graphs based on mutual following relationships between original posters. Saves graphs to `graphs/{HASHTAG}_root_graphs/`.

3.  **Sentiment Analysis (for Reply Networks):**
    *   `sentiment_analysis_vader.py`: Reads reply texts from `texts/`, performs sentiment analysis using VADER, and annotates nodes in the GEXF context graphs (`graphs/{HASHTAG}_graphs/`) with 'pos', 'neg', and 'compound' sentiment scores.

4.  **Echo-Chamber Detection & Analysis (Reply Networks):**
    *   `detect_echo_chambers.py`:
        *   Loads sentiment-annotated context graphs.
        *   Splits graphs into positive and negative sentiment subgraphs (based on the 'compound' score).
        *   Calculates the Clustering Coefficient for each subgraph.
        *   Identifies potential echo-chambers based on the paper's criteria (shared sentiment in a subgraph with CC >= 0.5, and/or no connectivity between opposing sentiment subgraphs).
        *   Visualizes these sentiment-separated subgraphs and saves them.
    *   `clustering_coefficient.py`:
        *   An alternative/focused script to calculate and visualize Clustering Coefficients for sentiment-based subgraphs in reply networks.
        *   *Note: This script uses a different sentiment splitting logic (based on `abs(positive)` vs `abs(negative)` scores) compared to `detect_echo_chambers.py`.*

5.  **Influential User Analysis (Original Toot Networks):**
    *   `co_citation.py`:
        *   Loads the original toot network graphs from `graphs/{HASHTAG}_root_graphs/`.
        *   Identifies the top 5 most influential users based on degree centrality (the paper also mentions betweenness centrality as a criterion).
        *   Loads the follower lists for these influential users from `roots/{HASHTAG}_roots/{USER_ID}_root_followers.json`.
        *   Calculates the normalized co-citation values for pairs of these influential users and the overall Normalized Common Reference Metric for the hashtag.

6.  **Visualization:**
    *   `visualize_graphs.py`: Provides general functionality to visualize the generated GEXF graphs (both context and root graphs), either with simple node labels or with sentiment attributes (if applicable).

## Prerequisites

*   Python 3.x
*   Libraries:
    *   `requests`
    *   `networkx`
    *   `matplotlib`
    *   `beautifulsoup4`
    *   `vaderSentiment`

You can typically install these using pip:
`pip install requests networkx matplotlib beautifulsoup4 vaderSentiment`
(Consider creating a `requirements.txt` file for easier dependency management.)

## How to Run

1.  **Configure Hashtags:** Modify the `hashtags` list in the relevant Python scripts to specify the sociopolitical hashtags for analysis.
2.  **Data Collection:**
    *   Run `get_hashtag_statuses.py`.
    *   Run `get_contexts.py`.
    *   Run `get_followings_of_repliers.py`.
    *   Run `collect_replies_text.py`.
    *   Run `get_followings_of_roots.py`.
    *   Run `get_followers_of_repliers.py` (to gather follower data for original posters for co-citation analysis).
3.  **Graph Construction:**
    *   Run `create_repliers_graph.py`.
    *   Run `create_roots_graph.py`.
4.  **Sentiment Analysis:**
    *   Run `sentiment_analysis_vader.py` (annotates reply network graphs).
5.  **Analysis & Detection:**
    *   For reply network echo-chambers: Run `detect_echo_chambers.py`. Optionally, run `clustering_coefficient.py` for a focused CC analysis with a different sentiment split.
    *   For influential user analysis: Run `co_citation.py`.
6.  **Visualization:**
    *   Use `visualize_graphs.py` as needed for additional graph visualizations.

## Data Format Examples

*   **Contexts (`_context.json`):** Standard Mastodon API V1 status context format, containing "ancestors" and "descendants" lists of status objects.
*   **Followings/Followers (`_followings.json`, `_followers.json`):** A JSON list of Mastodon account objects.
*   **Graphs (`.gexf`):** Standard GEXF format, viewable with tools like Gephi. Nodes representing repliers in context graphs will have sentiment attributes (`pos`, `neg`, `compound`) after `sentiment_analysis_vader.py` is run.
*   **Hashtag Statuses (`.json`):** A JSON list of Mastodon status objects.
*   **Reply Texts (`.txt`):** Plain text files where the first line is the replier's ID, and subsequent lines are their replies within that specific context.

## Citation

If you use this codebase or methodology, please cite the original research paper:
*Huitema, I. R., Oskooei, A. R., Aktaş, M. S., & Riveni, M. (2024, December). Investigating Echo-Chambers in Decentralized Social Networks: A Mastodon Case Study. In International Conference on Complex Networks and Their Applications (pp. 316-328). Cham: Springer Nature Switzerland.*
