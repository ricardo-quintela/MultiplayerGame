import pygame

from guiElements.window import Window, WindowEvent

from inverseKinematics import Bone, Skeleton



SIZE = (800,600)
FPS = 60

pygame.init()

def main():
    root = Window(SIZE, FPS)

    events = WindowEvent()


    # Criar um braco e um atenbraco
    braco = Bone(100, 100, 100, 0, "braco")
    antebraco = Bone(100, 100, 100, 0, "antebraco")

    # ligar o braco ao antebraco para que se movam juntos
    antebraco.bind(braco.a)

    # criar um esqueleto para colocar todos os ossos
    esqueleto = Skeleton()

    # colocar os ossos no esqueleto
    esqueleto.add(braco)
    esqueleto.add(antebraco)


    # criar um novo membro (ver docum de Limb)
    esqueleto.newLimb("membro")

    # adicionar os ossos ao membro pela ordem crescente (o primeiro a ser adicionado é o que vai ser fixado num ponto)
    esqueleto.getLimb("membro").add(esqueleto.getBone("antebraco"))
    esqueleto.getLimb("membro").add(esqueleto.getBone("braco"))


    # um ponto fixo para ligar o membro
    anchor = [400, 300]


    # fixar o membro num ponto "ancora"
    esqueleto.getLimb("membro").fixate(anchor)



    direction = 1


    while events.getEvent("windowState"):
        root.tick()

        # update the events
        events.eventsCheck()

        # fill the canvas with white
        root.fill("white")


        # movimentar a ancora para tras e para a frente
        anchor[0] += direction
        if anchor[0] < 200 or anchor[0] > 600:
            direction *= -1


        # user o objeto esqueleto para atualizar todos os ossos e suas posiçoes
        esqueleto.getBone("braco").follow(events.getEvent("mousePos"))
        esqueleto.update()
        esqueleto.blit(root.canvas)
        

        root.update()


if __name__ == "__main__":
    main()