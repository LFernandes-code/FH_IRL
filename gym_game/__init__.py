 
from gym.envs.registration import register

register(
    id= 'FlowerHunter-v0',
    entry_point= 'gym_game.envs:FHEnv',
    max_episode_steps=4000,
    kwargs={'map_name': "Level1"}
)