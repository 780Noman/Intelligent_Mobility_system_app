import GameEnv
import numpy as np
from ddqn_keras import DDQNAgent
import pygame
import os
import tensorflow as tf

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

model_path = "ddqn_model.keras"



TOTAL_GAMETIME = 1000
N_EPISODES = 10000
REPLACE_TARGET = 50

game = GameEnv.RacingEnv()
game.fps = 60

ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=5, epsilon=1.00, 
                        epsilon_end=0.10, epsilon_dec=0.9995, replace_target=REPLACE_TARGET, 
                        batch_size=512, input_dims=19, fname=model_path)

ddqn_scores = []
eps_history = []
best_score = float('-inf')  # Store highest score only

def run():
    global best_score
    for e in range(N_EPISODES):
        game.reset()
        done = False
        score = 0
        counter = 0
        observation_, reward, done = game.step(0)
        observation = np.array(observation_)
        gtime = 0
        renderFlag = e % 10 == 0 and e > 0  # Render every 10 episodes

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
            ddqn_agent.remember(observation, action, reward, observation_, int(done))
            observation = observation_
            ddqn_agent.learn()
            gtime += 1
            if gtime >= TOTAL_GAMETIME:
                done = True
            if renderFlag:
                game.render(action)

        eps_history.append(ddqn_agent.epsilon)
        ddqn_scores.append(score)
        avg_score = np.mean(ddqn_scores[max(0, e-100):(e+1)])

        # Save model only if it achieves a new highest score
        if score > best_score:
            best_score = score
            ddqn_agent.save_model()
            print(f"🎯 New best score {best_score}! Model saved.")

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ddqn_agent.update_network_parameters()
        
        print(f'Episode: {e}, Reward (Total): {int(score)}, Avg Reward: {int(avg_score)}, Best Reward: {int(best_score)}, Epsilon: {ddqn_agent.epsilon}')
run()
