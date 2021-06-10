(define (problem fighter) (:domain dnd_player)

    (:objects 
        ; Player
        player - player
        ; NPCs
        corvus - npc
        anvil - npc
        indifferent - indifferent
        friendly - friendly
        hostile - hostile
        ; Rooms
        stout_meal_inn - room
        inns_cellar - room
        storage_room - room
        burial_chamber - room
        western_corridor - room
        antechamber - room
        southern_corridor - room
        baradins_crypt - room
        ; Doors
        door1 - door
        door2 - door
        door3 - door
        door4 - door
        door5 - door
        door6 - door
        door7 - door
        ; Monsters
        cat - cat
        giant_rat1 - giant_rat
        giant_rat2 - giant_rat
        giant_rat3 - giant_rat
        giant_rat4 - giant_rat
        ; goblin1 - goblin
        ; goblin2 - goblin
        ; goblin3 - goblin
        ; skeleton - skeleton
        ; zombie - zombie
        ; Abilities
        cha - ability
        con - ability
        dex - ability
        int - ability
        str - ability
        wis - ability
        ; Skills
        perception - skill
        ; Equipment
        thieves_tools - equipment
        ; Weapons
        greataxe - weapon
        javelin - weapon
        crossbow_light - weapon
    )

    (:init
        ; =======================================
        ; Adventure
        ; (quest)

        ; =======================================
        ; Player
        (alive player)
        (at player stout_meal_inn)
        ; set abilities
        (charisma cha)
        (constitution con)
        (dexterity dex)
        (intelligence int)
        (strength str)
        (wisdom wis)
        ; set skills
        (perception perception)
        ; set weapons
        (has player greataxe)
        (has player javelin)
        (has player crossbow_light)
        ; set equipment
        (thieves_tools thieves_tools)
        (has player thieves_tools)

        ; =======================================
        ; NPCs
        (alive corvus)
        (alive anvil)
        (at corvus stout_meal_inn)
        (at anvil inns_cellar)
        (gives_quest corvus)
        ; set attitudes
        (attitude_towards_player corvus hostile)
        (attitude_towards_player anvil indifferent)
        (improve_attitude indifferent friendly)
        (improve_attitude hostile indifferent)
        (degrade_attitude friendly indifferent)
        (degrade_attitude indifferent hostile)

        ; =======================================
        ; Monsters
        (at giant_rat1 inns_cellar)
        (at giant_rat2 inns_cellar)
        (at giant_rat3 inns_cellar)
        (at giant_rat4 inns_cellar)
        ; (at goblin1 storage_room)
        ; (at goblin2 antechamber)
        ; (at goblin3 antechamber)
        ; (at skeleton burial_chamber)
        ; (at zombie storage_room)
        (alive giant_rat1)
        (alive giant_rat2)
        (alive giant_rat3)
        (alive giant_rat4)
        ; (alive goblin2)
        ; (alive goblin3)
        ; (alive skeleton)
        ; (alive zombie)

        ; =======================================
        ; Rooms
        (connected door1 stout_meal_inn inns_cellar)
        (connected door1 inns_cellar stout_meal_inn)
        (connected door2 inns_cellar storage_room)
        (connected door2 storage_room stout_meal_inn)
        (connected door3 storage_room burial_chamber)
        (connected door3 burial_chamber storage_room)
        (connected door4 storage_room western_corridor)
        (connected door4 western_corridor storage_room)
        (connected door5 western_corridor antechamber)
        (connected door5 antechamber western_corridor)
        (connected door6 antechamber southern_corridor)
        (connected door6 southern_corridor antechamber)
        (connected door7 southern_corridor baradins_crypt)
        (connected door7 baradins_crypt southern_corridor)
        (at door1 stout_meal_inn)
        (at door1 inns_cellar)
        (at door2 inns_cellar)
        (at door2 storage_room)
        (at door3 storage_room)
        (at door3 burial_chamber)
        (at door4 storage_room)
        (at door4 western_corridor)
        (at door5 western_corridor)
        (at door5 antechamber)
        (at door6 antechamber)
        (at door6 southern_corridor)
        (at door7 southern_corridor)
        (at door7 baradins_crypt)
        (locked door3)
        (locked door4)
        (locked door6)
        (locked door7)

        ; =======================================
        ; Combat
        (must_kill giant_rat1)
        (must_kill giant_rat2)
        (must_kill giant_rat3)
        (must_kill giant_rat4)
        ; (must_kill goblin2)
        ; (must_kill goblin3)
        ; (must_kill skeleton)
        ; (must_kill zombie)

        ; =======================================
        ; Challenges
        ; set DC for doors
        (dc door3 str)
        (dc door4 str)
        (dc door6 str)
        (dc door3 perception)
        (dc door4 perception)
        ; set equipment DC for doors
        (dc_equipment door6 thieves_tools)
        ; doors not broken are considered "alive"
        (alive door1)
        (alive door2)
        (alive door3)
        (alive door4)
        (alive door5)
        (alive door6)
        (alive door7)
    )

    (:goal (and
        (at player southern_corridor)
    ))
)
