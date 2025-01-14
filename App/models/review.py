# from App.controllers.command import get_votes_by_review
# from App.controllers.review import get_upvotes_by_review
from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from App.models.votecommand import VoteCommand


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    votes = db.Column(MutableDict.as_mutable(JSON), nullable=False)

    def __init__(self, user_id, student_id, text):
        self.user_id = user_id
        self.student_id = student_id
        self.text = text
        self.votes = {"num_upvotes": 0, "num_downvotes": 0}

    def vote(self, user_id, vote):
        self.votes.update({user_id: vote})
        self.votes.update(
            {"num_upvotes": len([vote for vote in self.votes.values() if vote == "up"])}
        )
        self.votes.update(
            {
                "num_downvotes": len(
                    [vote for vote in self.votes.values() if vote == "down"]
                )
            }
        )

    def get_num_upvotes(self):
        num_upvotes=0
        # votecommands = get_votes_by_review(review_id)
        votecommands= VoteCommand.query.filter_by(review_id=self.id)
        # votecommands = []
        for votecommand in votecommands:
            if votecommand.vote_type==1:
                num_upvotes+=1
        return num_upvotes

    def get_num_downvotes(self):
        num_downvotes=0
        # votecommands = get_votes_by_review(review_id)
        votecommands= VoteCommand.query.filter_by(review_id=self.id)
        for votecommand in votecommands:
            if votecommand.vote_type==-1:
                num_downvotes+=1
        return num_downvotes

    def get_karma(self):
        return self.get_num_upvotes() - self.get_num_downvotes()

    def get_all_votes(self):
        num_votes=0
        votecommands= VoteCommand.query.filter_by(review_id=self.id)
        for votecommand in votecommands:
            num_votes+= 1
        return num_votes

    def toJSON(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "text": self.text,
            "karma": self.get_karma(),
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
        }
