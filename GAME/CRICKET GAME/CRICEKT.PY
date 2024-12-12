import random
import time

class Player:
    def __init__(self, name, batting_skill, bowling_skill):
        self.name = name
        self.batting_skill = batting_skill
        self.bowling_skill = bowling_skill
        self.runs = 0
        self.balls_faced = 0
        self.wickets = 0
        self.balls_bowled = 0
        self.runs_conceded = 0

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.total_runs = 0
        self.wickets = 0
        self.overs = 0
        self.balls = 0

class Match:
    def __init__(self, team1, team2, overs):
        self.team1 = team1
        self.team2 = team2
        self.overs = overs
        self.current_batting_team = None
        self.current_bowling_team = None

    def toss(self):
        if random.choice([True, False]):
            self.current_batting_team, self.current_bowling_team = self.team1, self.team2
        else:
            self.current_batting_team, self.current_bowling_team = self.team2, self.team1
        print(f"{self.current_batting_team.name} won the toss and elected to bat.")

    def play_innings(self):
        batting_order = list(range(11))
        bowling_order = list(range(11))
        random.shuffle(bowling_order)
        
        current_batsmen = [0, 1]
        current_bowler = 0
        striker = 0

        print(f"\n{self.current_batting_team.name}'s innings begins!")

        while self.current_batting_team.overs < self.overs and self.current_batting_team.wickets < 10:
            self.current_batting_team.balls += 1
            batsman = self.current_batting_team.players[batting_order[current_batsmen[striker]]]
            bowler = self.current_bowling_team.players[bowling_order[current_bowler]]

            batsman.balls_faced += 1
            bowler.balls_bowled += 1

            delivery = self.bowl(bowler)
            outcome = self.bat(batsman, delivery)

            if outcome == "out":
                print(f"{batsman.name} is out after scoring {batsman.runs} runs!")
                self.current_batting_team.wickets += 1
                bowler.wickets += 1
                if self.current_batting_team.wickets < 10:
                    current_batsmen[striker] = max(current_batsmen) + 1
            else:
                runs = outcome
                batsman.runs += runs
                bowler.runs_conceded += runs
                self.current_batting_team.total_runs += runs
                print(f"{runs} runs scored")
                if runs % 2 == 1:
                    striker = 1 - striker

            if self.current_batting_team.balls == 6:
                self.current_batting_team.overs += 1
                self.current_batting_team.balls = 0
                print(f"End of over {self.current_batting_team.overs}. Score: {self.current_batting_team.total_runs}/{self.current_batting_team.wickets}")
                striker = 1 - striker
                current_bowler = (current_bowler + 1) % 11

            time.sleep(1)  # Add a small delay for readability

        print(f"{self.current_batting_team.name} innings ends. Total score: {self.current_batting_team.total_runs}/{self.current_batting_team.wickets} in {self.current_batting_team.overs}.{self.current_batting_team.balls} overs")

    def bowl(self, bowler):
        deliveries = ["pace", "spin", "yorker", "bouncer"]
        return random.choices(deliveries, weights=[40, 30, 15, 15])[0]

    def bat(self, batsman, delivery):
        base_prob = {
            "dot": 20,
            "single": 30,
            "double": 10,
            "four": 10,
            "six": 5,
            "out": 10
        }

        # Adjust probabilities based on batsman skill and delivery type
        if delivery == "pace":
            base_prob["out"] += 5
            base_prob["four"] += 5
        elif delivery == "spin":
            base_prob["single"] += 10
            base_prob["dot"] -= 5
        elif delivery == "yorker":
            base_prob["dot"] += 10
            base_prob["out"] += 5
        elif delivery == "bouncer":
            base_prob["out"] += 5
            base_prob["six"] += 5

        # Apply batsman's skill
        base_prob["out"] = max(5, base_prob["out"] - batsman.batting_skill // 10)
        base_prob["four"] += batsman.batting_skill // 20
        base_prob["six"] += batsman.batting_skill // 30

        outcome = random.choices(list(base_prob.keys()), weights=list(base_prob.values()))[0]
        
        if outcome == "dot":
            return 0
        elif outcome == "single":
            return 1
        elif outcome == "double":
            return 2
        elif outcome == "four":
            return 4
        elif outcome == "six":
            return 6
        else:
            return "out"

    def display_scoreboard(self, team):
        print(f"\nScoreboard for {team.name}:")
        print(f"{'Player':<20}{'Runs':<10}{'Balls':<10}{'Wickets':<10}")
        print("-" * 50)
        for player in team.players:
            if player.balls_faced > 0 or player.balls_bowled > 0:
                print(f"{player.name:<20}{player.runs:<10}{player.balls_faced:<10}{player.wickets:<10}")
        print(f"\nTotal: {team.total_runs}/{team.wickets} in {team.overs}.{team.balls} overs")

    def play_match(self):
        self.toss()
        self.play_innings()
        self.display_scoreboard(self.current_batting_team)
        
        target = self.current_batting_team.total_runs + 1
        print(f"\nTarget for {self.current_bowling_team.name}: {target} runs")

        self.current_batting_team, self.current_bowling_team = self.current_bowling_team, self.current_batting_team
        self.current_batting_team.total_runs = 0
        self.current_batting_team.wickets = 0
        self.current_batting_team.overs = 0
        self.current_batting_team.balls = 0

        self.play_innings()
        self.display_scoreboard(self.current_batting_team)

        if self.current_batting_team.total_runs >= target:
            print(f"{self.current_batting_team.name} wins by {10 - self.current_batting_team.wickets} wickets!")
        elif self.current_batting_team.total_runs == target - 1:
            print("The match is a tie!")
        else:
            print(f"{self.current_bowling_team.name} wins by {target - self.current_batting_team.total_runs - 1} runs!")

def create_player(name):
    batting_skill = random.randint(50, 100)
    bowling_skill = random.randint(50, 100)
    return Player(name, batting_skill, bowling_skill)

def create_team(name):
    return Team(name, [create_player(f"Player {i+1}") for i in range(11)])

if __name__ == "__main__":
    team1 = create_team("Team A")
    team2 = create_team("Team B")
    match = Match(team1, team2, overs=20)
    match.play_match()
    