# print(len([x for x in input().split(' ') if x!='' and x[0]!=' ' ]))


year=int(input())

animals=['Обезьяна','Петух','Собака','Свинья','Крыса','Бык','Тигр','Заяц','Дракон','Змея','Лошадь','Овца']


print(animals[year%12])

