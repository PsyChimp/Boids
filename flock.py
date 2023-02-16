import random
import pygame
import math3d
import math
import time
class Boid(object):
    def __init__(self,bounding,obstacles):
            self.bounding=list(bounding)
            self.x=random.randint(bounding[0],bounding[2])
            self.y=random.randint(bounding[1],bounding[3])
            self.obstacles=obstacles
            self.bp1=bounding[0]+10
            self.bp2=bounding[1]+10
            self.bp3=bounding[2]-10
            self.bp4=bounding[3]-10
            self.boidPos=math3d.VectorN(self.x,self.y)
            self.velocity=math3d.VectorN(random.uniform(-10,10),random.uniform(-10,10))
            self.orientation=math.atan2(-self.velocity[1],self.velocity[0])
            self.distance=0
            for obs in self.obstacles:
                for i in range(0,3):
                    distance=self.boidPos-obs[i][0]
                    self.distance=distance
                    if self.distance.magnitude()<=obs[i][1]+15:
                        
                        self.x=random.randint(bounding[0],bounding[2])
                        self.y=random.randint(bounding[1],bounding[3])
                        self.boidPos=math3d.VectorN(self.x,self.y)
            if random.randint(0,3)==0:
                self.type="Predator"
            else:
                self.type="Prey"
    def update(self,deltaTime,mpos,flock_point_1,flock_point_2,velocity):
        
        self.boidPos+=self.velocity*deltaTime
        
        
        
        
        if (self.velocity.magnitude())==0:
            self.beak1=self.boidPos[0]+10*math.cos(self.orientation)
            self.beak2=self.boidPos[1]-10*math.sin(self.orientation)
            self.beakPos=math3d.VectorN(self.beak1,self.beak2)
        else:
            self.velNorm=self.velocity.normalized()
            self.velPerp=math3d.VectorN(-self.velNorm[1],self.velNorm[0])
            self.orientation=math.atan2(-self.velocity[1],self.velocity[0])
            self.beakPos=self.boidPos+10*self.velocity.normalized()
            self.fin1=self.boidPos+self.velPerp*5
            self.fin2=self.boidPos-self.velPerp*5
        if self.boidPos[0]<self.bp1:
            self.velocity[0]*=-.5
            self.boidPos[0]=self.bp1
        if self.boidPos[0]>self.bp3:
            self.velocity[0]*=-.5
            self.boidPos[0]=self.bp3
        if self.boidPos[1]<self.bp2:
            self.velocity[1]*=-.5
            self.boidPos[1]=self.bp2
        if self.boidPos[1]>self.bp4:
            self.velocity[1]*=-.5
            self.boidPos[1]=self.bp4
            
        if self.velocity[0]>15:
            self.velocity[0]=15
        if self.velocity[0]<-15:
            self.velocity[0]=-15

        if self.velocity[1]>15:
            self.velocity[1]=15
        if self.velocity[1]<-15:
            self.velocity[1]=-15

        if mpos!=None:
            mousedir=mpos-self.boidPos
            self.velocity+=10*mousedir.normalized()*deltaTime
        else:
            pass
        if flock_point_1!=False and self.type=="Predator":
            flock_dir_1=flock_point_1-self.boidPos
            self.velocity+=20*flock_dir_1.normalized()*deltaTime
        if flock_point_2!=False and self.type=="Prey":
            flock_dir_2=flock_point_2-self.boidPos
            self.velocity+=20*flock_dir_2.normalized()*deltaTime
        else:
            pass
        if velocity!=False:
            self.velocity+=20*velocity.normalized()*deltaTime

        for obs in self.obstacles:
            for i in range(0,3):
                distance=self.boidPos-obs[i][0]
                self.distance=distance
                if self.distance.magnitude()<=obs[i][1]+20:
                    self.velocity+=50*distance.normalized()*deltaTime
        
    def render(self,surface):


        pygame.draw.line(surface,(255,255,255),self.boidPos.int(),self.beakPos.int())
        if self.type=="Predator":
            pygame.draw.polygon(surface,(200,0,0),(self.fin1.int(),self.fin2.int(),self.beakPos.int()),1)
        else:
            pygame.draw.polygon(surface,(0,200,0),(self.fin1.int(),self.fin2.int(),self.beakPos.int()),1)
class Flock(object):
    def __init__(self,bounding,flock_size,obstacles):
        self.num_pred=0
        self.num_prey=0
        self.boid_list=[]
        self.obstacles=[obstacles] 
        
        
        for i in range(0,flock_size):
            i=Boid(bounding,self.obstacles)
            self.boid_list.append(i)
        for boid in self.boid_list:
            if boid.type=="Predator":
                self.num_pred+=1
            else:
                self.num_prey+=1
        
        
    def update(self,deltaTime,mpos):
        self.flock_vec1=math3d.VectorN(0,0)
        self.flock_vec2=math3d.VectorN(0,0)
        for boid in self.boid_list:
            if boid.type=="Predator":
                self.flock_vec1+=boid.boidPos
            else:
                self.flock_vec2+=boid.boidPos
            
        self.flock_vec1/=self.num_pred
        self.flock_vec2/=self.num_prey

        self.velocity=math3d.VectorN(0,0)

        for boid in self.boid_list:
            self.velocity+=boid.velocity
            

        self.velocity/=len(self.boid_list)

        distance=self.flock_vec1-self.flock_vec2

        for boid in self.boid_list:
            if boid.type=="Prey":
                self.velocity=40*distance.normalized()*deltaTime
            if boid.type=="Predator":
                self.velocity-=40*distance.normalized()*deltaTime
        
        for boid in self.boid_list:
            boid.update(deltaTime,mpos,self.flock_vec1,self.flock_vec2,self.velocity)

    def render(self,surface):
        for boid in self.boid_list:
            boid.render(surface)
