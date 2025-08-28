import GameEnv
import numpy as np
from ddqn_keras import DDQNAgent
import pygame
import tensorflow as tf

# model_path = "ddqn_model.keras"
model_path="ddqn_model.keras"

try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f" Failed to load model: {e}")

TOTAL_GAMETIME = 10000
N_EPISODES = 10000
REPLACE_TARGET = 10

game = GameEnv.RacingEnv()
game.fps = 60

ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=5, epsilon=0.02, 
                        epsilon_end=0.01, epsilon_dec=0.999, replace_target=REPLACE_TARGET, 
                        batch_size=64, input_dims=19, fname=model_path)

ddqn_agent.load_model()
ddqn_agent.update_network_parameters()

def run():
    for e in range(N_EPISODES):
        game.reset()
        done = False
        score = 0
        counter = 0
        gtime = 0
        observation_, reward, done = game.step(0)
        observation = np.array(observation_)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            action = ddqn_agent.choose_action(observation)
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)

            if reward == 0:
                counter += 1
                if counter > 100:
                    done = True
            else:
                counter = 0

            score += reward
            observation = observation_
            gtime += 1
            if gtime >= TOTAL_GAMETIME:
                done = True
            game.render(action)
            #  if score > best_score:
            # best_score = score
            # ddqn_agent.save_model()
            # print(f" New best score {best_score}! Model saved.")

        print(f"Episode: {e}, Reward: {score}")

run()
