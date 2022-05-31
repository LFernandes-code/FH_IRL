from re import S
import pygame
import pygame.locals
import time
import math
import random
import numpy as np
from datetime import datetime
import os

from sqlalchemy import false

MAP_HEIGHT = 600
MAP_WIDTH = 600


def get_center(sprite):
	return (sprite.rect.x + sprite.rect.width/2, sprite.rect.y + sprite.rect.height/2)


class Follower(pygame.sprite.Sprite):

	hp_provided = -5

	perception_distance = 200

	value = 1

	hp = 50

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		image_name = "Images/Dark_ghost.png"
		self.image = pygame.image.load(image_name)
		x_size, y_size = self.image.get_rect().size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.x_size = x_size
		self.y_size = y_size
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.mask = pygame.mask.from_surface(self.image)
		self.world = world

	def collided(self):
		self.kill()



	def update(self):

		distance = math.sqrt((self.world.player.rect.x - self.rect.x )**2 + (self.world.player.rect.y - self.rect.y)**2 )

		if distance <= self.perception_distance:

			self.x_pos += (self.world.player.rect.x - self.x_pos)/distance

			self.y_pos += (self.world.player.rect.y - self.y_pos)/distance

			image_name = "Images/Dark_ghost.png"
			self.image = pygame.image.load(image_name)
			x_size, y_size = self.image.get_rect().size
			self.rect = pygame.Rect(self.x_pos, self.y_pos, x_size, y_size)
			self.x_size = x_size
			self.y_size = y_size
			self.mask = pygame.mask.from_surface(self.image)

		else:
			image_name = "Images/Tent_ghost.png"
			self.image = pygame.image.load(image_name)
			x_size, y_size = self.image.get_rect().size
			self.rect = pygame.Rect(self.x_pos, self.y_pos, x_size, y_size)
			self.x_size = x_size
			self.y_size = y_size
			self.mask = pygame.mask.from_surface(self.image)

		self.rect.x = self.x_pos

		self.rect.y = self.y_pos

		if self.world.player.is_collided_with(self):

			self.x_pos -= 8*(self.world.player.rect.x - self.x_pos)/distance

			self.y_pos -= 8*(self.world.player.rect.y - self.y_pos)/distance

			self.rect.x = self.x_pos

			self.rect.y = self.y_pos

			self.world.player.hp += self.hp_provided

		for weapon in self.world.weapon_group:
			if weapon.is_collided_with(self):
				self.hp -= weapon.damage

				self.world.player.damage_done += weapon.damage

				self.x_pos -= weapon.throwback*(self.world.player.rect.x - self.x_pos)/distance

				self.y_pos -= weapon.throwback*(self.world.player.rect.y - self.y_pos)/distance

				self.rect.x = self.x_pos

				self.rect.y = self.y_pos

		if self.hp <= 0:
			self.kill()
			self.world.player.enemy_killed += 1


class Player(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.max_hp = 100

		self.enemy_killed = 0

		self.hp = 100

		self.money = 0

		self.damage_done = 0

		self.imagined_x = 0
		self.imagined_y = 0

		self.image = pygame.image.load("Images/30-30_samurai_ball_3.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class Sword(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world, angle):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.lifetime = 3
		self.angle = angle
		self.damage = 10
		self.throwback = 20

		self.image = pygame.transform.rotate(pygame.image.load("Images/sword.png"), self.angle)
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def update(self):
		self.lifetime -= 1

		if self.lifetime <= 0:
			self.kill()


class Flower(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world


		self.image = pygame.image.load("Images/Flower.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass

	def get_pos(self):
		return self.rect.x, self.rect.y


class Money(pygame.sprite.Sprite):

	value = 1

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		self.money_provided = 1


		self.image = pygame.image.load("Images/money.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos + 4, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		
		if self.is_collided_with(self.world.player):
			self.world.player.money += self.money_provided

			self.kill()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def get_pos(self):
		return self.rect.x, self.rect.y


class RiceCake(pygame.sprite.Sprite):

	value = 1

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		self.hp_provided = 10


		self.image = pygame.image.load("Images/Rice_cake_20_20.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		
		if self.is_collided_with(self.world.player):
			self.world.player.hp += self.hp_provided

			if self.world.player.hp > self.world.player.max_hp:
				self.world.player.hp = self.world.player.max_hp

			self.kill()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def get_pos(self):
		return self.rect.x, self.rect.y


class Tile(pygame.sprite.Sprite):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world


		self.image = pygame.image.load("Images/30-30_red_ball.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass

	def get_pos(self):
		return self.rect.x, self.rect.y


class GrassTile(Tile):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		number = random.randint(0,3)
		image_name = "Images/20-20_grass_square" + str(number) + ".png"
		self.image = pygame.image.load(image_name)
		x_size, y_size = self.image.get_rect().size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


class RockWall(Tile):

	def __init__(self, x_pos, y_pos, world):

		pygame.sprite.Sprite.__init__(self)
		self.world = world

		number = random.randint(0,3)
		image_name = "Images/20-20_rock_wall" + str(number) + ".png"
		self.image = pygame.image.load(image_name).convert_alpha()
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.initial_x = x_pos
		self.initial_y = y_pos
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass


class Polygon(pygame.sprite.Sprite):

	def __init__(self, world, points, number):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.rect = (0,0)

		self.number = number

		self.points = points

	
		self.image = pygame.Surface((self.world.screen_width, self.world.screen_height), pygame.SRCALPHA)

		#self.image.set_alpha(0)

		pygame.draw.polygon(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), points)

		self.image = self.image.convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		pass



	def draw(self, screen):
		screen.blit(self.image, (0,0))


class Iterator_Square(pygame.sprite.Sprite):

	def __init__(self, world, granularity):

		self.world = world
		self.granularity = granularity

		self.rect = pygame.Rect(0, 0, self.granularity, self.granularity)

		self.image = pygame.Surface((self.granularity, self.granularity), pygame.SRCALPHA)

		pygame.draw.rect(self.image, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), self.rect)

		self.image = self.image.convert_alpha()

		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x, self.rect.y))


class Perceptor(object):

	def __init__(self, world, frequency, date_time, map_name, num_directions):

		self.world = world
		self.player = world.player
		self.frequency = frequency
		self.num_directions = num_directions

		self.fader_can_write = False

		self.polygon_group = pygame.sprite.Group()

		self.create_polygons()

		


		self.distance_closest_enemy = float('inf')
		self.distance_closest_food_item = float('inf')
		self.distance_closest_money = float('inf')
		self.distance_to_objective = float('inf')
		self.number_enemies_view = 0
		self.number_food_item_view = 0
		self.number_money_view = 0
		self.sum_enemy_values = 0   #How dangerous an enemy is. The highest, the more dangerous the enemy
		self.sum_food_item_values = 0    #How valuable an item is. The highest, the more valuable the item
		self.sum_money_values = 0
		self.sum_value_slash_distance_enemies = 0
		self.sum_value_slash_distance_food_item = 0
		self.sum_value_slash_distance_money = 0
		self.seconds_since_enemy = 0
		self.seconds_since_food_item = 0
		self.seconds_since_money = 0

		self.max_distance = abs(math.sqrt((self.world.screen_width/2) ** 2 + (self.world.screen_height/2) ** 2))

		self.hp = self.player.hp
		self.kills = 0
		self.money = 0
		self.damage_done = 0

		self.to_save_buffer = []
		self.current_perceptions = []


		self.last_enemy_time = time.time()
		self.last_food_item_time = time.time()
		self.last_money_time = time.time()

		self.last_update = time.time()

		file_name = "Traces/Perceptor_" + map_name + "_" + date_time + ".txt"
		self.save_file = open(file_name,"w+")


	def create_polygons(self):

		if self.num_directions % 4 != 0:
			print("The variable num_directions must be divisible by 4!")
			exit()

		#Draw top polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((i*(self.world.screen_width/(self.num_directions/4)),0), ((i+1)*(self.world.screen_width/(self.num_directions/4)),0), get_center(self.player)), ((self.num_directions/4)/2 + i) ))

		#Draw left polygons
		for i in range(int(self.num_directions/4)):

			if i < (self.num_directions/4)/2:
				self.polygon_group.add(Polygon(self.world, ((0, self.world.screen_height - i*(self.world.screen_height/(self.num_directions/4))), (0, self.world.screen_height - (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), ( self.num_directions*3/4 + (self.num_directions/4)/2 + i) ) )
			else:
				self.polygon_group.add(Polygon(self.world, ((0, self.world.screen_height - i*(self.world.screen_height/(self.num_directions/4))), (0, self.world.screen_height - (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), (i - (self.num_directions/4)/2 ) ))


		#Draw right polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((self.world.screen_width, i*(self.world.screen_height/(self.num_directions/4))), (self.world.screen_width, (i+1)*(self.world.screen_height/(self.num_directions/4))), get_center(self.player)), ( self.num_directions/4 + (self.num_directions/4)/2 + i)))

		#Draw bottom polygons
		for i in range(int(self.num_directions/4)):
			self.polygon_group.add(Polygon(self.world, ((self.world.screen_width - i*(self.world.screen_width/(self.num_directions/4)), self.world.screen_width), (self.world.screen_width - (i+1)*(self.world.screen_width/(self.num_directions/4)), self.world.screen_width), get_center(self.player)), ( (self.num_directions*2)/4 + (self.num_directions/4)/2 + i)))







	def update(self):

		self.current_perceptions = []

		if (time.time() - self.last_update) > 1/self.frequency:

			previous_distance_closest_enemy = self.distance_closest_enemy
			self.number_enemies_view = 0
			self.sum_enemy_values = 0
			self.distance_closest_enemy = float('inf')
			self.sum_value_slash_distance_enemies = 0
			for enemy in self.world.enemy_group:
				if self.world.in_view(enemy):
					self.last_enemy_time = time.time()
					self.number_enemies_view += 1
					self.sum_enemy_values += enemy.value
					distance = math.sqrt((self.player.rect.x - enemy.rect.x )**2 + (self.player.rect.y - enemy.rect.y)**2 )
					self.sum_value_slash_distance_enemies += enemy.value*10/distance
					if distance < self.distance_closest_enemy:
						self.distance_closest_enemy = distance

			self.seconds_since_enemy = int(time.time() - self.last_enemy_time)


			previous_distance_closest_money = self.distance_closest_money
			self.number_money_view = 0
			self.sum_money_values = 0
			self.distance_closest_money = float('inf')
			self.sum_value_slash_distance_money = 0
			for money in self.world.money_group:
				if self.world.in_view(money):
					self.last_money_time = time.time()
					self.number_money_view += 1
					self.sum_money_values += money.value
					distance = math.sqrt((self.player.rect.x - money.rect.x )**2 + (self.player.rect.y - money.rect.y)**2 )
					self.sum_value_slash_distance_money += money.value*10/distance
					if distance < self.distance_closest_money:
						self.distance_closest_money = distance

			self.seconds_since_money = int(time.time() - self.last_money_time)						



			#updating distance_closest_food
			previous_distance_closest_food_item = self.distance_closest_food_item
			self.number_food_item_view = 0
			self.sum_food_item_values = 0
			self.distance_closest_food_item = float('inf')
			self.sum_value_slash_distance_food_item = 0
			for food in self.world.food_group:
				if self.world.in_view(food):
					self.last_food_item_time = time.time()
					self.number_food_item_view += 1
					self.sum_food_item_values += food.value
					distance = math.sqrt((self.player.rect.x - food.rect.x )**2 + (self.player.rect.y - food.rect.y)**2 )
					self.sum_value_slash_distance_food_item += food.value*10/distance
					if distance < self.distance_closest_food_item:
						self.distance_closest_food_item = distance

			self.seconds_since_food_item = int(time.time() - self.last_food_item_time)

			
			previous_distance_to_objective = self.distance_to_objective 
			for flower in self.world.flower_group:
				if self.world.in_view(flower):
					distance = math.sqrt((self.player.rect.x - flower.rect.x )**2 + (self.player.rect.y - flower.rect.y)**2 )
					self.distance_to_objective = distance

			self.hp = self.player.hp

			self.kills = self.player.enemy_killed

			self.money = self.player.money


			self.damage_done = self.world.player.damage_done


			#save data

			self.current_perceptions.append(str(self.distance_closest_enemy) + "_")  #
			self.current_perceptions.append(str(self.distance_closest_food_item) + "_")  #
			self.current_perceptions.append(str(self.distance_closest_money) + "_")
			self.current_perceptions.append(str(self.number_enemies_view) + "_")  #
			self.current_perceptions.append(str(self.number_food_item_view) + "_")  #
			self.current_perceptions.append(str(self.number_money_view) + "_")  #
			self.current_perceptions.append(str(self.sum_enemy_values) + "_") 
			self.current_perceptions.append(str(self.sum_food_item_values) + "_") 
			self.current_perceptions.append(str(self.sum_money_values) + "_")  
			self.current_perceptions.append(str(self.sum_value_slash_distance_enemies) + "_")  #
			self.current_perceptions.append(str(self.sum_value_slash_distance_food_item) + "_")  #
			self.current_perceptions.append(str(self.sum_value_slash_distance_money) + "_")
			self.current_perceptions.append(str(self.seconds_since_enemy) + "_")  #
			self.current_perceptions.append(str(self.seconds_since_food_item) + "_")  #
			self.current_perceptions.append(str(self.seconds_since_money) + "_")  #
			self.current_perceptions.append(str(self.distance_to_objective) + "_")  #
			self.current_perceptions.append(str(self.hp) + "_")  #
			self.current_perceptions.append(str(self.money) + "_")  #
			self.current_perceptions.append(str(self.kills) + "_")  #
			self.current_perceptions.append(str(self.damage_done) + "_")  # 
			


			#Neutrals
			#print("Neutrals")
			neutral_vec = self.get_perception_vec(self.world.collide_group)
			self.current_perceptions.append(str(neutral_vec.tolist())+ "_")

			#Desirables
			#print("Desirables")
			desirable_vec = self.get_perception_vec(self.world.money_group)
			self.current_perceptions.append(str(desirable_vec.tolist()) + "_")

			#Conditionals 
			#print("Conditionals")
			conditional_vec = self.get_perception_vec(self.world.food_group)
			self.current_perceptions.append(str(conditional_vec.tolist()) + "_")

			#Enemies
			#print("Enemies")
			enemies_vec = self.get_perception_vec(self.world.enemy_group)
			self.current_perceptions.append(str(enemies_vec.tolist()) + "_")

			#Objective
			#print("Objectives")
			objective_vec = self.get_perception_vec(self.world.flower_group)
			self.current_perceptions.append(str(objective_vec.tolist()))

			self.current_perceptions.append("\n")


			self.last_update = time.time()


			self.fader_can_write = True

			self.to_save_buffer.extend(self.current_perceptions)

	def get_perception_vec(self, relevant_group):

		myX, myY = get_center(self.player)

		dist_q_array = np.full((1, self.num_directions), 0)

		for poppy in relevant_group:

			# Checking if inside screen
			if (poppy.rect.x > -poppy.x_size) and (poppy.rect.x < self.world.screen_width) and (poppy.rect.y > -poppy.y_size) and (poppy.rect.y < self.world.screen_height):

				targetX, targetY = get_center(poppy)


				collided = pygame.sprite.spritecollide(poppy, self.polygon_group, False, pygame.sprite.collide_mask)

				#print("Have collided with:")
				for polly in collided:
					#print(polly.number)
					distance = math.hypot(targetX - myX, targetY - myY)
					
					if abs(self.max_distance - distance) > dist_q_array[0][int(polly.number)]:

							dist_q_array[0][int(polly.number)] = abs(self.max_distance - distance)
						

				# myradians = math.atan2(targetY - myY, targetX - myX)
				# # print("My radians: ", myradians)
				# pos_radians = myradians + math.pi
				# quadrant = int(pos_radians // ((2 * math.pi) / self.num_directions))
				# if quadrant == self.num_directions:
				# 	quadrant -= 1
				# distance = math.hypot(targetX - myX, targetY - myY)
				# # print(distance)

				# if abs(distance) <= self.max_distance:

				# 	if abs(self.max_distance - distance) > dist_q_array[0][quadrant]:

				# 		dist_q_array[0][quadrant] = abs(self.max_distance - distance)
				
			# print(type(poppy).__name__)
		#print(dist_q_array)
		return dist_q_array



	def write_to_file(self):

		for savvy in self.to_save_buffer:
			self.save_file.write(savvy)

		self.save_file.close()




	def render(self):




		distance_closest_enemy_rend = self.world.font.render("Distance to closest enemy: " + str(self.distance_closest_enemy), 1, (0,0,0))
		self.world.screen.blit(distance_closest_enemy_rend, (10, 50))

		distance_closest_food_item_rend = self.world.font.render("Distance to closest food/item: " + str(self.distance_closest_food_item), 1, (0,0,0))
		self.world.screen.blit(distance_closest_food_item_rend, (10, 70))

		distance_closest_money_rend = self.world.font.render("Distance to closest coin: " + str(self.distance_closest_money), 1, (0,0,0))
		self.world.screen.blit(distance_closest_money_rend, (10, 90))

		distance_to_objective_rend = self.world.font.render("Distance to objective: " + str(self.distance_to_objective), 1, (0,0,0))
		self.world.screen.blit(distance_to_objective_rend, (10, 110))

		number_enemies_view_rend = self.world.font.render("Number of enemies in view: " + str(self.number_enemies_view), 1, (0,0,0))
		self.world.screen.blit(number_enemies_view_rend, (10, 130))

		number_food_item_view_rend = self.world.font.render("Number of food/items in view: " + str(self.number_food_item_view), 1, (0,0,0))
		self.world.screen.blit(number_food_item_view_rend, (10, 150))

		number_money_view_rend = self.world.font.render("Number of coins in view: " + str(self.number_money_view), 1, (0,0,0))
		self.world.screen.blit(number_money_view_rend, (10, 170))

		sum_enemy_values_rend = self.world.font.render("Sum of enemy values: " + str(self.sum_enemy_values), 1, (0,0,0))
		self.world.screen.blit(sum_enemy_values_rend, (10, 190))

		sum_food_item_values_rend = self.world.font.render("Sum of food/item values: " + str(self.sum_food_item_values), 1, (0,0,0))
		self.world.screen.blit(sum_food_item_values_rend, (10, 210))

		sum_money_values_rend = self.world.font.render("Sum of coin values: " + str(self.sum_money_values), 1, (0,0,0))
		self.world.screen.blit(sum_money_values_rend, (10, 230))

		sum_value_slash_distance_enemies_rend = self.world.font.render("Sum of value/distance for all enemies: " + str(self.sum_value_slash_distance_enemies), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_enemies_rend, (10, 250))

		sum_value_slash_distance_food_item_rend = self.world.font.render("Sum of value/distance for all food/items: " + str(self.sum_value_slash_distance_food_item), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_food_item_rend, (10, 270))

		sum_value_slash_distance_money_rend = self.world.font.render("Sum of value/distance for all coins: " + str(self.sum_value_slash_distance_money), 1, (0,0,0))
		self.world.screen.blit(sum_value_slash_distance_money_rend, (10, 290))

		seconds_since_enemy_rend = self.world.font.render("Seconds since new enemy spotted: " + str(self.seconds_since_enemy), 1, (0,0,0))
		self.world.screen.blit(seconds_since_enemy_rend, (10, 310))

		seconds_since_food_item_rend = self.world.font.render("Seconds since new food/item spotted: " + str(self.seconds_since_food_item), 1, (0,0,0))
		self.world.screen.blit(seconds_since_food_item_rend, (10, 330))

		seconds_since_money_rend = self.world.font.render("Seconds since new coins spotted: " + str(self.seconds_since_money), 1, (0,0,0))
		self.world.screen.blit(seconds_since_money_rend, (10, 350))
	
		hp_rend = self.world.font.render("HP: " + str(self.hp), 1, (0,0,0))
		self.world.screen.blit(hp_rend, (10, 370))

		money_rend = self.world.font.render("Coins: " + str(self.money), 1, (0,0,0))
		self.world.screen.blit(money_rend, (10, 390))

		kills_rend = self.world.font.render("Kills: " + str(self.kills), 1, (0,0,0))
		self.world.screen.blit(kills_rend, (10, 410))

		damage_done_rend = self.world.font.render("Damage Done: " + str(self.damage_done), 1, (0,0,0))
		self.world.screen.blit(damage_done_rend, (10, 430))


		pygame.display.flip()


class World(object):


# WORLD TYPES:
# infinite
# load
# load infinite


	def __init__(self, screen_width, screen_height, tile_size, world_type, small_fontzy):


		self.speed = 5


		self.x_pos = 0
		self.y_pos = 0

		self.world_type = world_type

		self.timer = time.time()
		

		#0 -> not shifting
		#1 -> key to shift is pressed but the opposite key was pressed afterwards and has priority
		#2 -> shifting
		self.shift_left = 0
		self.shift_right = 0
		self.shift_up = 0
		self.shift_down = 0

		self.ticker = 0

		self.key_press_list = []

		self.key_press_to_write = []
		self.pos_to_write = []


		self.tile_size = tile_size

		self.all_group = pygame.sprite.Group()
		self.tile_group = pygame.sprite.Group()
		self.collide_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.food_group = pygame.sprite.Group()
		self.money_group = pygame.sprite.Group()
		self.flower_group = pygame.sprite.Group()
		self.weapon_group = pygame.sprite.Group()
		self.player = None

		self.screen_width = screen_width
		self.screen_height = screen_height

		self.grass_surface = None

		if self.world_type == "infinite":
			pass
			#TODO
			#self.matrix =  Matrix(int(self.screen_height/tile_size), int(self.screen_width/tile_size), self)
		elif self.world_type == "load infinite":
			pass
			# TODO
		else:
			self.load(self.world_type)


		self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
		self.font = small_fontzy
		self.last_food = time.time()

		self.iterator_square = Iterator_Square(self, 20)

		



	def load(self, file_name):

		file_path = "Maps/" + file_name + ".csv"

		f = open(file_path, "r")
		lines = f.readlines()

		player_x = 0
		player_y = 0



		self.grass_surface = pygame.Surface((len(lines[0])*self.tile_size, len(lines)*self.tile_size))

		self.grass_surface.fill((255,255,255))


		line_count = 0
		for line in lines:
			column_count = 0
			line = line.replace('	', '')
			line = line.replace(';', '')

			for letter in line:

				if letter == '.':

					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == '0':
					tilly = Flower(column_count*self.tile_size, line_count*self.tile_size, self)
					self.flower_group.add(tilly)
					self.all_group.add(tilly)
				elif letter == '\n':
					pass
				elif letter == ' ':
					pass
				elif letter == '	':
					pass		
				elif letter == '_':
					pass		
				elif letter == "r":
					ricy = RiceCake(column_count*self.tile_size + 5, line_count*self.tile_size + 5, self)
					self.food_group.add(ricy)
					self.all_group.add(ricy)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == "m":
					muuney = Money(column_count*self.tile_size, line_count*self.tile_size, self)
					self.money_group.add(muuney)
					self.all_group.add(muuney)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == 'f':
					new_follower = Follower(column_count*self.tile_size, line_count*self.tile_size, self)
					self.enemy_group.add(new_follower)
					self.all_group.add(new_follower)
					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)

				elif letter == 'x':
					wally = RockWall(column_count*self.tile_size, line_count*self.tile_size, self)
					self.collide_group.add(wally)
					self.all_group.add(wally)
				elif letter == "p":
					player_x = column_count*self.tile_size
					player_y = line_count*self.tile_size


					# #To Remove
					# self.playerx = column_count*self.tile_size
					# self.playery = line_count*self.tile_size


					tilly = GrassTile(column_count*self.tile_size, line_count*self.tile_size, self)
					self.tile_group.add(tilly)



				column_count += 1
			line_count += 1

		for dudette in self.all_group:
			dudette.rect.x += self.screen_height/2 -15 - player_x
			dudette.rect.y += self.screen_width/2 -15 - player_y

		for tillete in self.tile_group:
			tillete.rect.x += self.screen_height/2 -15 - player_x
			tillete.rect.y += self.screen_width/2 -15 - player_y

		for folly in self.enemy_group:
			folly.x_pos += self.screen_height/2 -15 - player_x
			folly.y_pos += self.screen_width/2 -15 - player_y



		for grasser in self.tile_group:
			self.grass_surface.blit(grasser.image, grasser.rect)


	def check_x_movement(self):



		if self.shift_left == 2:

			for pop in self.collide_group:
				pop.rect.x = pop.rect.x - self.speed

			self.player.imagined_x += self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.x = pop.rect.x + self.speed
					self.player.imagined_x -= self.speed
					return


			for flower in self.flower_group:
				flower.rect.x = flower.rect.x - self.speed

			for enem in self.enemy_group:
				enem.x_pos = enem.x_pos - self.speed

			for food in self.food_group:
				food.rect.x = food.rect.x - self.speed

			for money in self.money_group:
				money.rect.x = money.rect.x - self.speed
			
		elif self.shift_right == 2:

			for pop in self.collide_group:
				pop.rect.x = pop.rect.x + self.speed

			self.player.imagined_x -= self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.x = pop.rect.x - self.speed
					self.player.imagined_x += self.speed
					return

			for flower in self.flower_group:
				flower.rect.x = flower.rect.x + self.speed


			for enem in self.enemy_group:
				enem.x_pos = enem.x_pos + self.speed

			for food in self.food_group:
				food.rect.x = food.rect.x + self.speed

			for money in self.money_group:
				money.rect.x = money.rect.x + self.speed

			
	def check_y_movement(self):


		if self.shift_up == 2:

			for pop in self.collide_group:
				pop.rect.y = pop.rect.y - self.speed

			self.player.imagined_y += self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.y = pop.rect.y + self.speed
					self.player.imagined_y -= self.speed
					return


			for flower in self.flower_group:
				flower.rect.y = flower.rect.y - self.speed

			for enem in self.enemy_group:
				enem.y_pos = enem.y_pos - self.speed

			for food in self.food_group:
				food.rect.y = food.rect.y - self.speed

			for money in self.money_group:
				money.rect.y = money.rect.y - self.speed
			
		elif self.shift_down == 2:

			for pop in self.collide_group:
				pop.rect.y = pop.rect.y + self.speed

			self.player.imagined_y -= self.speed

			for poppy in self.collide_group:
				if self.player.is_collided_with(poppy):
					for pop in self.collide_group:
						pop.rect.y = pop.rect.y - self.speed
					self.player.imagined_y += self.speed
					return

			for flower in self.flower_group:
				flower.rect.y = flower.rect.y + self.speed


			for enem in self.enemy_group:
				enem.y_pos = enem.y_pos + self.speed

			for food in self.food_group:
				food.rect.y = food.rect.y + self.speed

			for money in self.money_group:
				money.rect.y = money.rect.y + self.speed
			
	def in_view(self, sprity):

		if sprity.rect.x >= (0 - sprity.x_size) and sprity.rect.x <= self.screen_width and sprity.rect.y >= (0 - sprity.y_size) and sprity.rect.y <= self.screen_height:
			return True
		else:
			return False


	def get_all_in_view(self, sprite_group):

		in_view = []

		for sprity in sprite_group:
			if self.in_view(sprity):
				in_view.append(sprity)

		return in_view


	def update(self):

		self.key_press_list = []
		self.key_press_list.append(self.ticker)

		self.check_x_movement()

		self.check_y_movement()

		self.all_group.update()
		self.player.update()

		self.ticker += 1


	def update_matrix(self):
		pass



	def render(self):

		self.screen.fill((255,255,255))


		self.screen.blit(self.grass_surface, (-self.player.imagined_x,-self.player.imagined_y))
		self.collide_group.draw(self.screen)
		self.flower_group.draw(self.screen)
		self.food_group.draw(self.screen)
		self.money_group.draw(self.screen)
		self.enemy_group.draw(self.screen)
		self.weapon_group.draw(self.screen)
		self.player.draw(self.screen)



		self.iterator_square.draw(self.screen)




		hp_rend = self.font.render("HP: " + str(self.player.hp), 1, (0,0,0))
		self.screen.blit(hp_rend, (10, 10))

		money_rend = self.font.render("Coins: " + str(self.player.money), 1, (0,0,0))
		self.screen.blit(money_rend, (200, 10))

		kill_rend = self.font.render("Kills: " + str(self.player.enemy_killed), 1, (0,0,0))
		self.screen.blit(kill_rend, (310, 10))

		time_rend = self.font.render("Time: " + str(int(time.time() - self.timer)), 1, (0,0,0))
		self.screen.blit(time_rend, (400, 10))


class Value_Point(pygame.sprite.Sprite):

	def __init__(self, world, x_pos, y_pos):

		pygame.sprite.Sprite.__init__(self)
		self.world = world
		self.image = pygame.image.load("Images/black_square_4.png")
		x_size, y_size = self.image.get_rect().size
		self.x_size = x_size
		self.y_size = y_size
		self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, screen):
		screen.blit(self.image, self.rect)

	def render(self):
		screen = self.world.screen
		self.draw(screen)


class LimitlessFader(pygame.sprite.Sprite):


	def __init__(self, world):

		self.world = world
		self.value_points_group = pygame.sprite.Group()

		self.rising = 0
		self.lowering = 0

		self.value = 0


	def update(self):

		value = 0

		if self.rising == 2:
			value = 1

		elif self.lowering == 2:
			value = -1

		for vally in self.value_points_group:
			vally.rect.x -= 1
			vally.rect.y += 3*value

		self.value += value

		new_square = Value_Point(self.world, self.world.screen_width - 100, self.world.screen_height/2 - 2)
		self.value_points_group.add(new_square)

	def render(self):

		for vally in self.value_points_group:
			vally.render()



	def normalize(self, value):

		#To implement

		return value

# game
class PyGame2D:
	def __init__(self, map_name) -> None:
		pygame.init()
		logo = pygame.image.load("Images/30-30_samurai_ball_3.png")
		pygame.display.set_icon(logo)
		pygame.display.set_caption("Flower Hunter")

		
		self.clock = pygame.time.Clock()

		self.frame_rate = 0.0
		self.screeno = pygame.display.set_mode([MAP_HEIGHT, MAP_WIDTH])

		big_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 62)
		medium_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 32)
		small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)
		self.fonts = [small_fontzy, medium_fontzy, big_fontzy]

		date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + "_" + str(random.randint(0, 1000))

		self.map_name = map_name

		self.num_directions = 200 #Needs to be divisable by 8

		#self.running = True
		self.world = World(MAP_HEIGHT, MAP_WIDTH, 20, self.map_name, self.fonts[0])
		self.player = Player(self.world.screen_width/2 -15, self.world.screen_height/2 -15, self.world)
		self.world.player = self.player
		self.perceptor = Perceptor(self.world, 8, date_time, map_name, self.num_directions)
		self.player_dead = False
		self.player_won = False
		self.key_up = -1
		self.key_down = -1
		self.last_sword_parameters = [12, -15, 0]


	def action(self, action):
		self.last_update = time.time()
		#update playing_routine
		self.world.update()
		#handle death
		if self.world.player.hp <= 0:
			self.world.player.hp = 0
			self.player_dead = True

		self.last_sword_parameters = set_sword_parameters(self.world, self.last_sword_parameters)
		
		#check objective
		for flower in self.world.flower_group:
			if self.player.is_collided_with(flower):
				self.player_won = True

		#convert action to key
		action_keys = [pygame.locals.K_RIGHT, pygame.locals.K_LEFT, pygame.locals.K_UP, pygame.locals.K_DOWN, pygame.locals.K_SPACE]
		if action != 5:
			#create the event
			if action != self.key_down:
				newevent_down = pygame.event.Event(pygame.locals.KEYDOWN, key=action_keys[action], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_down)
				self.key_down = action
			else:
				self.key_down = -1
				#create the event
				newevent_down = pygame.event.Event(pygame.locals.KEYUP, key=action_keys[action], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_down)
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				handle_key_down(self.world, event.key, self.last_sword_parameters)
			if event.type == pygame.KEYUP:
				handle_key_up(self.world, event.key, self.last_sword_parameters)
		

	def observe(self):
		#read perceptor
		pass
	
	def evaluate(self):
		reward = 0
		if self.player_dead:
			reward = -10000 + self.perceptor.distance_to_objective
		elif self.player_won:
			reward = 10000 
		# add reward based of % coins collected
		reward += (self.perceptor.money * 1000)
		# add reward based of % enemies killed
		reward += (self.perceptor.kills * 1000)
		return reward

	def is_done(self):
		if self.player_dead or self.player_won:
			return True
        
		return False

	def view(self):
        #display play routine
		self.world.render()
		pygame.display.flip()
		self.clock.tick(60)

def handle_key_down(world, event_key, last_sword_parameters):

	if event_key == ord(' '):

		world.key_press_list.append(' ')
		swordy = Sword(world.player.rect.x + last_sword_parameters[0], world.player.rect.y + last_sword_parameters[1], world, last_sword_parameters[2])
		world.weapon_group.add(swordy)
		world.all_group.add(swordy)

	if event_key == pygame.K_LEFT or event_key == ord('a'):

		world.key_press_list.append('ad')
		if world.shift_left == 2:

			world.shift_left = 1
			world.shift_right = 2
		else:
			world.shift_right = 2

	if event_key == pygame.K_RIGHT or event_key == ord('d'):

		world.key_press_list.append('dd')
		if world.shift_right == 2:

			world.shift_right = 1
			world.shift_left = 2
		else:
			world.shift_left = 2

	if event_key == pygame.K_UP or event_key == ord('w'):

		world.key_press_list.append('wd')
		if world.shift_up == 2:

			world.shift_up = 1
			world.shift_down = 2
		else:
			world.shift_down = 2

	if event_key == pygame.K_DOWN or event_key == ord('s'):

		world.key_press_list.append('sd')
		if world.shift_down == 2:

			world.shift_down = 1
			world.shift_up = 2
		else:
			world.shift_up = 2


def handle_key_up(world, event_key, last_sword_parameters):



	if event_key == pygame.K_LEFT or event_key == ord('a'):

		world.key_press_list.append('au')
		if world.shift_left == 1:
			world.shift_right = 0
			world.shift_left = 2
		else:
			world.shift_right = 0

	if event_key == pygame.K_RIGHT or event_key == ord('d'):

		world.key_press_list.append('du')
		if world.shift_right == 1:
			world.shift_left = 0
			world.shift_right = 2
		else:
			world.shift_left = 0

	if event_key == pygame.K_UP or event_key == ord('w'):

		world.key_press_list.append('wu')
		if world.shift_up == 1:
			world.shift_down = 0
			world.shift_up = 2
		else:
			world.shift_down = 0

	if event_key == pygame.K_DOWN or event_key == ord('s'):

		world.key_press_list.append('su')
		if world.shift_down == 1:
			world.shift_up = 0
			world.shift_down = 2
		else:
			world.shift_up = 0


def set_sword_parameters(world, last_sword_parameters):

	if world.shift_down == 2 and world.shift_right == 2:
			last_sword_parameters = [-8, -8, 45]

	elif world.shift_down == 2 and world.shift_left == 2:
		last_sword_parameters = [22, -8, 315]

	elif world.shift_up == 2 and world.shift_right == 2:
		last_sword_parameters = [-8, 22, 135]

	elif world.shift_up == 2 and world.shift_left == 2:
		last_sword_parameters = [22, 22, 225]

	elif world.shift_down == 2:
		last_sword_parameters = [12, -15, 0]
	elif world.shift_up == 2:
		last_sword_parameters = [12, 30, 180]
	elif world.shift_right == 2:
		last_sword_parameters = [-15, 12, 90]
	elif world.shift_left == 2:
		last_sword_parameters = [30, 12, 270]	

	return last_sword_parameters

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	game = PyGame2D("Level1",0)

















