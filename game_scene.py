# This scene shows the main game.

from scene import *
import ui
import sound
from numpy import random
#from copy import deepcopy


class GameScene(Scene):
    def setup(self):
        # this method is called, when user moves to this scene

        # Set to zero
        self.score = 0
        self.highscore = 0
        self.did_user_die = False

        #self.size_of_screen = deepcopy(self.size)
        #self.center_of_screen = deepcopy(self.size/2)

        # updated to not use deepcopy
        self.size_of_screen_x = self.size.x
        self.size_of_screen_y = self.size.y
        self.screen_center_x = self.size_of_screen_x/2
        self.screen_center_y = self.size_of_screen_y/2

        self.left_button_down = False
        self.right_button_down = False

        #self.ship_move_speed = 20.0
        self.ship_move_speed = 25.0

        self.missiles = []
        self.aliens = []

        self.alien_attack_rate = 1
        self.alien_attack_speed = 20.0

        self.scale_size = 0.75 #Adjust size of the sprites

        # add background color
        background_position = Vector2(self.screen_center_x,
                                      self.screen_center_y)
        self.background = SpriteNode('./assets/sprites/star_background.png',
                                     position = background_position,
                                     parent = self,
                                     size = self.size)

        spaceship_position = Vector2()
        spaceship_position.x = self.screen_center_x
        spaceship_position.y = 100
        self.spaceship = SpriteNode('./assets/sprites/spaceship.png',
                                    parent = self,
                                    position = spaceship_position,
                                    scale = self.scale_size)

        left_button_position = Vector2()
        left_button_position.x = 100
        left_button_position.y = 100
        self.left_button = SpriteNode('./assets/sprites/left_button.png',
                                      parent = self,
                                      position = left_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_size)

        right_button_position = Vector2()
        right_button_position.x = 300
        right_button_position.y = 100
        self.right_button = SpriteNode('./assets/sprites/right_button.png',
                                       parent = self,
                                       position = right_button_position,
                                       alpha = 0.5,
                                       scale = self.scale_size)

        fire_button_position = Vector2()
        fire_button_position.x = self.size_of_screen_x - 100
        fire_button_position.y = 100
        self.fire_button = SpriteNode('./assets/sprites/red_button.png',
                                      parent = self,
                                      position = fire_button_position,
                                      alpha = 0.5,
                                      scale = self.scale_size)

        score_label_position = Vector2()
        score_label_position.x = 100
        score_label_position.y = self.size_of_screen_y - 100
        self.score_label = LabelNode(text = 'Score: ',
                                      font=('Helvetica', 20),
                                      parent = self,
                                      position = score_label_position,
                                      scale = 0.75)

        high_score_label_position = Vector2()
        high_score_label_position.x = self.size_of_screen_x - 100
        high_score_label_position.y = self.size_of_screen_y - 100
        self.high_score_label = LabelNode(text = 'Highscore: ',
                                      font=('Helvetica', 20),
                                      parent = self,
                                      position = high_score_label_position,
                                      scale = 0.75)

        #If died then draw main menu button
        if self.did_user_die == True:
            self.go_back_button = SpriteNode('plf:AlienBlue_climb1',
                                          parent = self,
                                          position = Vector2(self.screen_center_x, self.screen_center_y),
                                          scale = self.scale_size)


    def update(self):
        # this method is called, hopefully, 60 times a second

        # move spaceship if button down
        if (self.spaceship.position.x - self.ship_move_speed)> 100: # restrict domain for the ship
            # move spaceship if button down
            if self.left_button_down == True:
                self.spaceship.run_action(Action.move_by(-1*self.ship_move_speed,                           0.0, 0.1))


        if (self.spaceship.position.x + self.ship_move_speed) < self.size_of_screen_x-100: # restrict domain for the ship
            if self.right_button_down == True:
                self.spaceship.run_action(Action.move_by(self.ship_move_speed, 0.0, 0.1))



        # every update, randomly check if a new alien should be created
        alien_create_chance = random.randint(1, 120)
        if alien_create_chance <= self.alien_attack_rate:
            self.add_alien()

        # check every update if a missile is off screen
        for missile in self.missiles:
            if missile.position.y > self.size_of_screen_y + 50:
                missile.remove_from_parent()
                self.missiles.remove(missile)
                #print('missile removed')


        # check every update if an alien is off screen
        #print(len(self.aliens))
        for alien in self.aliens:
            if alien.position.y < -50:
                alien.remove_from_parent()
                self.aliens.remove(alien)
                # you might want to end the game, or take points away
                if self.did_user_die== False: #if game not ended then
                    self.score= self.score - 2 #Lose 2 points


        # check every update to see if a missile has touched a space alien
        if len(self.aliens) > 0 and len(self.missiles) > 0:
            #print('missile check')
            for alien in self.aliens:
                for missile in self.missiles:
                    if alien.frame.intersects(missile.frame):
                        missile.remove_from_parent()
                        self.missiles.remove(missile)
                        alien.remove_from_parent()
                        self.aliens.remove(alien)
                        # since you destroyed one, make more show up
                        #self.alien_attack_rate = self.alien_attack_rate + 1
                        if self.did_user_die== False: #if game not ended then
                            self.score= self.score + 1 #Get a point
        else:
            pass
            #print(len(self.aliens))

        # check every update to see alien touches spaceship
        if len(self.aliens) > 0:
            #print('checking')
            for alien_hit in self.aliens:
                #print('alien ->' + str(alien_hit.frame))
                #print('ship  ->' + str(self.spaceship.frame))
                if alien_hit.frame.intersects(self.spaceship.frame):
                    #print('a hit')
                    self.spaceship.remove_from_parent()
                    alien_hit.remove_from_parent()
                    self.aliens.remove(alien_hit)

                    # since game over, move to next scene
        else:
            pass
            #print(len(self.aliens))


        #Get highscore
        if self.score > self.highscore:
            self.highscore= self.score


        #Update label
        self.score_label.text= 'Score: ' + str(self.score)
        self.high_score_label.text= 'Highscore: ' + str(self.highscore)





    def touch_began(self, touch):
        # this method is called, when user touches the screen

        # check if left or right button is down
        if self.left_button.frame.contains_point(touch.location):
            self.left_button_down = True

        if self.right_button.frame.contains_point(touch.location):
            self.right_button_down = True

    def touch_moved(self, touch):
        # this method is called, when user moves a finger around on the screen
        pass

    def touch_ended(self, touch):
        # this method is called, when user releases a finger from the screen

        # if start button is pressed, goto game scene
        if self.fire_button.frame.contains_point(touch.location):
            sound.play_effect('laser1.wav') #Play music
            sound.stop_effect('laser1.wav') #Stop music
            #Need to stop music after playing
            self.create_new_missile('missile.png') #Play music

        else:
            # if I removed my finger, then no matter what spaceship
            #    should not be moving any more
            self.left_button_down = False
            self.right_button_down = False

    def did_change_size(self):
        # this method is called, when user changes the orientation of the screen
        # thus changing the size of each dimension
        pass

    def pause(self):
        # this method is called, when user touches the home button
        # save anything before app is put to background
        pass

    def resume(self):
        # this method is called, when user place app from background
        # back into use. Reload anything you might need.
        pass

    def create_new_missile(self):
        # when the user hits the fire button

        missile_start_position = Vector2()
        missile_start_position.x = self.spaceship.position.x
        missile_start_position.y = 100

        missile_end_position = Vector2()
        missile_end_position.x = missile_start_position.x
        missile_end_position.y = self.size_of_screen_y + 100

        self.missiles.append(SpriteNode('./assets/sprites/missile.png',
                             position = missile_start_position,
                             parent = self))

        # make missile move forward
        missileMoveAction = Action.move_to(missile_end_position.x,
                                           missile_end_position.y + 100,
                                           5.0)
        self.missiles[len(self.missiles)-1].run_action(missileMoveAction)

    def add_alien(self):
        # add a new alien to come down

        alien_start_position = Vector2()
        alien_start_position.x = random.randint(100,
                                         self.size_of_screen_x - 100)
        alien_start_position.y = self.size_of_screen_y + 100

        alien_end_position = Vector2()
        alien_end_position.x = random.randint(100,
                                        self.size_of_screen_x - 100)
        alien_end_position.y = -100

        self.aliens.append(SpriteNode('./assets/sprites/alien.png',
                             position = alien_start_position,
                             parent = self))

        # make missile move forward
        alienMoveAction = Action.move_to(alien_end_position.x,
                                         alien_end_position.y,
                                         self.alien_attack_speed,
                                         TIMING_SINODIAL)
        self.aliens[len(self.aliens)-1].run_action(alienMoveAction)
