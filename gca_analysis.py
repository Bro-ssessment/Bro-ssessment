import psycopg2

from brossessment.models import Post, postgres_db
import argparse
import sys
import re

def main():
    db = DatabaseConnection()
   
    users = db.get_users()


    result = {}
    for user_id in users:
        # try:
        db.gca(user_id[0])
        # except Exception:
        #     print("{} fail to fetch user ".format(user_id))
    
    #     for user_id in users:

    #         try:
    #             db.gca(user_id)

    #         except Exception:
    #             print("{} fail to fetch user ".format(user_id))
    
    # db.__del__() 


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(host="localhost",database="brosessment19", user="yonael")
        self.cursor = self.connection.cursor()

        
            # print("Cannot connect to database")
    
    
    def get_users(self):
        self.cursor.execute("SELECT distinct user_id from posts")
        users = self.cursor.fetchall()
        return users 


    # does the GCA Analysis 
    # Participation: Mean participation of an individual relative to the expected average of the group of its size
    # Internal Cohesion: How consistent an individual is with their own recent contributions
    # Responsivity: The tendency of an individual to respond, or not, to the previous contributions of their collaborative peers
    # Social Impact: The tendency of a participant to evoke corresponding responses from their collaborative peers
    # Newness: Whether one is likely to provide new information or to echo existing information
    # Communication Density: The extent to which participants convey information in a concise manner
    def gca(self, user_id):
        classes = self.get_classes(user_id)
        for class_id in classes:
            participation_score = self.participation(user_id, class_id[0])
            social_score = self.social_impact(user_id, class_id[0])
            print("User ID = {}, Class ID = {}, Participation Score = {}, Social Score = {}".format(user_id, class_id[0], participation_score, social_score))
        #     social_score = self.social_impact(user_id, class_id)
        #     print("Participation Score = %s \n Social Score = %s", participation_score, social_score)


            
            

    def get_classes(self, user_id):
        self.cursor.execute("SELECT distinct class_id from posts where user_id = {};".format(user_id))
        classes = self.cursor.fetchall()
        return classes 



    # Calculating the MEAN participation of the user in their class forum
    def participation(self, user_id, class_id):
        self.cursor.execute("SELECT count(distinct topic_id) from posts where class_id = {};".format(class_id))
        total = self.cursor.fetchall()


        self.cursor.execute("SELECT count(distinct topic_id) from posts where class_id = {} and user_id = {};".format(class_id, user_id))
        participated = self.cursor.fetchall()
  
        participation_score = (float(participated[0][0]) / float(total[0][0]))
        precision = ('{0:.3f}'.format(participation_score))

        return precision



    # how replied_to is each post on average, chance of being responded to
    
    #select count(replied_to) from replies where replied_to = 11637 and c_id = 4; 
    def social_impact(self, user_id, class_id):
        self.cursor.execute("SELECT count(replied_to) from replies where replied_to = {} and c_id = {};".format(user_id, class_id))
        replies = self.cursor.fetchall()

        self.cursor.execute("SELECT count(post_id) from posts where user_id = {} and class_id = {};".format(user_id, class_id))
        total_posts = self.cursor.fetchall()

        social_score = (float(replies[0][0])/float(total_posts[0][0]))
        precision = ('{0:.3f}'.format(social_score))
        return precision

    #select count(replied_to) from replies where replied_to = 1179 and c_id = 1; 
    #select count(post_id) from posts where user_id= 1179 and class_id = 1; 






# if __name__ == '__main__':
#     # In case error happen, start from where it broke
#     arg_parser = argparse.ArgumentParser()
#     arg_parser.add_argument(
#         "--begin_id", help="The ID of last parsed post ID", default=0
#     )
#     arg_parser.add_argument("--batch_size", help="Batch size", default=100)
#     arguments = arg_parser.parse_args()
#     main(arguments.begin_id, arguments.batch_size)

main()