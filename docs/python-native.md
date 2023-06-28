## Ваше решение написано на языке Python
Если ваше решение написано на языке Python, то для облегчения отправки ответа на платформу, вы можете упаковать его в модуль и импортировать в класс SolutionDemo (_baseline/solution/implementation/solution_demo.py_).
Далее, метод get_solution, который в базовой версии выглядит вот  - 
```python
    def get_solution(self):
        ## make magic with epicrisis
        return self.__DEMO_SOLUTION
```
Можно было бы преобразовать в нечто вроде - 
```python
    def get_solution(self):
        markup = MarkupSuperAI()
        solution = markup.analyze(self.epicrisis.path_to_xml)
        return solution
```
В случае, если метод асинхронный - сделать метод асинхронным.

## Для включения этого режима необходимо перевести значения env в -
```dotenv
SESSION_IS_ONLY_SAVE_FILES=
CHECK_DIRECTORY_ANSWER=
CHECK_DIRECTORY_ANSWER_DELAY=0
```


> Однако, вы можете воспользоваться и не привязанным к ЯП способом отправить своё решение на платформу [через файл в директории](/docs/to-directory.md);