import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


def lambda_handler():
    reddit = praw.Reddit('bot1')
    subs = ["unitedkingdom", "ukpolitics", "AskUK"]
    #subreddit = reddit.subreddit("unitedkingdom")
    #subreddit = reddit.subreddit("UKPersonalFinance")
    #subreddit = reddit.subreddit("ukpolitics")


    final_pos = 0
    final_neg = 0
    for s in subs:
        print(f'In subreddit {s}')
        subreddit = reddit.subreddit(s)

        top_posts = subreddit.hot(limit=10)
        import pdb;
        positive_score=0
        negative_score=0
        for post in top_posts:
            #print(post.title, post.score)
            if post.stickied:
                continue # jump over annoucements
            #print("\n --------")


            score = 0.0

            post.comments.replace_more(limit=None)

            for comment in post.comments.list():

                if comment.score >= 1:
                    sentiment_score= analyzer.polarity_scores(comment.body)
                    score += sentiment_score['compound']

                    #print(comment.body, sentiment_score)

            #print(f"At end: for {post.title},  score = {score} ")
            if score > 0:
                positive_score +=1
            else:
                negative_score += 1

        print(f" For subreddit {s} Final positive = {positive_score} negative = {negative_score}")
        final_pos += positive_score
        final_neg += negative_score

    print(f"At the end: {final_pos} {final_neg}")

    return final_pos, final_neg
