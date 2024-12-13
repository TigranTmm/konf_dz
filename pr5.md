# Практическое занятие №5. Вопросы виртуализации

## Задача 1

Исследование виртуальной стековой машины CPython.

Изучите возможности просмотра байткода ВМ CPython.

```Python
import dis

def foo(x):
    while x:
        x -= 1
    return x + 1

print(dis.dis(foo))
```

Опишите по шагам, что делает каждая из следующих команд (приведите эквивалентное выражение на Python):
```Python
 11           0 LOAD_FAST                0 (x)
              2 LOAD_CONST               1 (10)
              4 BINARY_MULTIPLY
              6 LOAD_CONST               2 (42)
              8 BINARY_ADD
             10 RETURN_VALUE
```

## Решение:

### Байткод:

```Python
11  0 LOAD_FAST                0 (x)           # Загружает значение переменной x (0 - это индекс переменной)
    2 LOAD_CONST               1 (10)          # Загружает константу 10
    4 BINARY_MULTIPLY                          # Умножает значение x на 10
    6 LOAD_CONST               2 (42)          # Загружает константу 42
    8 BINARY_ADD                               # Сложение результата предыдущего умножения с 42
   10 RETURN_VALUE                             # Возвращает итоговое значение
```

### Описание команд:

Допустим, при `x = 7`:

1. **`11 0 LOAD_FAST 0 (x)`**  
   Загружает значение переменной `x` (в данном случае `7`) на стек.

2. **`2 LOAD_CONST 1 (10)`**  
   Загружает константу `10` на стек.

3. **`4 BINARY_MULTIPLY`**  
   Умножает два верхних значения на стеке: `7 * 10`, что дает `70`. Результат `70` помещается на вершину стека.

4. **`6 LOAD_CONST 2 (42)`**  
   Загружает константу `42` на стек.

5. **`8 BINARY_ADD`**  
   Складывает два верхних значения на стеке: `70 + 42`, что дает `112`. Результат `112` становится новым верхним значением стека.

6. **`10 RETURN_VALUE`**  
   Возвращает верхнее значение со стека, т.е. `112`, как результат функции.

**Эквивалентный Python-код при `x = 7`:**

```python
result = (7 * 10) + 42  # result = 70 + 42 = 112
return result
```

**Результат выполнения кода**: `112`.


## Задача 2

Что делает следующий байткод (опишите шаги его работы)? Это известная функция, назовите ее.

```Python
  5           0 LOAD_CONST               1 (1)
              2 STORE_FAST               1 (r)

  6     >>    4 LOAD_FAST                0 (n)
              6 LOAD_CONST               1 (1)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       30

  7          12 LOAD_FAST                1 (r)
             14 LOAD_FAST                0 (n)
             16 INPLACE_MULTIPLY
             18 STORE_FAST               1 (r)

  8          20 LOAD_FAST                0 (n)
             22 LOAD_CONST               1 (1)
             24 INPLACE_SUBTRACT
             26 STORE_FAST               0 (n)
             28 JUMP_ABSOLUTE            4

  9     >>   30 LOAD_FAST                1 (r)
             32 RETURN_VALUE
```

## Решение:

Этот байткод представляет собой реализацию известной функции — **факториала**.

### Описание байткода и его эквивалента на Python:

Функция рассчитывает факториал числа `n` в императивном стиле (с использованием цикла).

#### Байткод с комментариями:

```python
  5           0 LOAD_CONST               1 (1)      # Загружает константу 1
              2 STORE_FAST               1 (r)      # Сохраняет значение 1 в переменную r

  6     >>    4 LOAD_FAST                0 (n)      # Загружает значение n
              6 LOAD_CONST               1 (1)      # Загружает константу 1
              8 COMPARE_OP               4 (>)      # Проверяет, больше ли n 1
             10 POP_JUMP_IF_FALSE       30          # Если n <= 1, переходит к адресу 30 (завершение)

  7          12 LOAD_FAST                1 (r)      # Загружает значение r
             14 LOAD_FAST                0 (n)      # Загружает значение n
             16 INPLACE_MULTIPLY                      # Умножает r на n
             18 STORE_FAST               1 (r)      # Сохраняет результат обратно в r

  8          20 LOAD_FAST                0 (n)      # Загружает значение n
             22 LOAD_CONST               1 (1)      # Загружает константу 1
             24 INPLACE_SUBTRACT                      # Вычитает 1 из n
             26 STORE_FAST               0 (n)      # Сохраняет результат обратно в n
             28 JUMP_ABSOLUTE            4          # Переходит к началу цикла (проверка условия n > 1)

  9     >>   30 LOAD_FAST                1 (r)      # Загружает значение r (итоговый результат)
             32 RETURN_VALUE                        # Возвращает r как результат функции
```

### Шаги выполнения байткода:

1. **`0 LOAD_CONST 1 (1)`**  
   Загружает константу `1` на стек.

2. **`2 STORE_FAST 1 (r)`**  
   Сохраняет значение `1` в локальную переменную `r`.  
   **Итог:** `r = 1`.

3. **`4 LOAD_FAST 0 (n)`**  
   Загружает значение переменной `n` на стек (это входной параметр функции,
   который определяет начальное значение `n`).

5. **`6 LOAD_CONST 1 (1)`**  
   Загружает константу `1` на стек.

6. **`8 COMPARE_OP 4 (>)`**  
   Сравнивает `n` и `1`, проверяя, больше ли `n` единицы. Если `n > 1`, результатом будет `True`, иначе — `False`.

7. **`10 POP_JUMP_IF_FALSE 30`**  
   Если результат предыдущего сравнения `False` (т.е., если `n <= 1`), то выполнение переходит
   на инструкцию по адресу `30`. Это завершит цикл, если `n <= 1`.

8. **`12 LOAD_FAST 1 (r)`**  
   Загружает текущее значение `r` на стек.

9. **`14 LOAD_FAST 0 (n)`**  
   Загружает текущее значение `n` на стек.

10. **`16 INPLACE_MULTIPLY`**  
   Умножает `r` на `n` и сохраняет результат в `r`.  
   **Итог:** `r = r * n`.

11. **`18 STORE_FAST 1 (r)`**  
    Сохраняет результат умножения в переменную `r`.

12. **`20 LOAD_FAST 0 (n)`**  
    Загружает текущее значение `n` на стек.

13. **`22 LOAD_CONST 1 (1)`**  
    Загружает константу `1` на стек.

14. **`24 INPLACE_SUBTRACT`**  
    Вычитает `1` из `n` и сохраняет результат в `n`.  
    **Итог:** `n = n - 1`.

15. **`26 STORE_FAST 0 (n)`**  
    Сохраняет результат в переменную `n`.

16. **`28 JUMP_ABSOLUTE 4`**  
    Возвращается к инструкции по адресу `4`, повторяя цикл, пока `n > 1`.

17. **`30 LOAD_FAST 1 (r)`**  
    Загружает текущее значение `r` на стек (результат цикла).

18. **`32 RETURN_VALUE`**  
    Возвращает значение `r` как результат функции.

### Анализ функции

Этот байткод реализует **факториал** числа `n`. Цикл умножает `r` на `n`, 
затем уменьшает `n` на `1`, повторяя это до тех пор, пока `n` не станет равным `1`. 
Переменная `r` накапливает произведение всех чисел от `n` до `1`.

### Эквивалентный Python-код

Эквивалентный код функции на Python, вычисляющей факториал:

```python
def factorial(n):
    r = 1
    while n > 1:
        r *= n
        n -= 1
    return r
```

**Ответ**: Это функция **факториала** (`factorial`).


## Задача 3

Приведите результаты из задач 1 и 2 для виртуальной машины JVM (Java) или .Net (C#).

## Решение:

### Задача 1 (выражение `x * 10 + 42`):
```java
import java.util.Scanner;

public class Task1 {
    public static int calculate(int x) {
        return x * 10 + 42;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter number x: ");
        int x = scanner.nextInt();

        int result = calculate(x);
        System.out.println("Result is: " + result);
    }
}
```

## Результат:

![image](https://github.com/user-attachments/assets/ae4fc9dc-4712-4ef9-a3dd-c340fd173eb8)


### Байткод JVM для задачи 1

Скомпилируем этот код и посмотрим байткод JVM для метода `compute`:

```
// public static int compute(int x);
0: iload_0          // загружает аргумент x (переменная 0)
1: bipush 10        // загружает константу 10
3: imul             // выполняет умножение x * 10
4: bipush 42        // загружает константу 42
6: iadd             // выполняет сложение (x * 10) + 42
7: ireturn          // возвращает результат
```

**Пояснение шагов:**

1. **`iload_0`** — Загружает значение переменной `x` на стек.
2. **`bipush 10`** — Загружает константу `10` на стек.
3. **`imul`** — Умножает два верхних значения на стеке, результат помещается на вершину стека.
4. **`bipush 42`** — Загружает константу `42` на стек.
5. **`iadd`** — Складывает два верхних значения на стеке, результат снова помещается на стек.
6. **`ireturn`** — Возвращает верхнее значение со стека как результат метода.


### Задача 2 (факториал):

```java
import java.util.Scanner;

public class Task2 {
    public static int factorial(int n) {
        int r = 1;
        while (n > 1) {
            r *= n;
            n -= 1;
        }
        return r;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number to calculate the factorial: ");
        int n = scanner.nextInt();

        int result = factorial(n);
        System.out.println("Result of factorial: " + result);
    }
}
```

### Байткод JVM для задачи 2

Для этого метода `factorial` байткод JVM будет следующим:

```
// public static int factorial(int n);
0: iconst_1         // загружает константу 1 для r
1: istore_1         // сохраняет значение 1 в переменную r
2: iload_0          // загружает значение n
3: iconst_1         // загружает константу 1
4: if_icmple 18     // переходит на 18, если n <= 1
7: iload_1          // загружает r
8: iload_0          // загружает n
9: imul             // выполняет умножение r * n
10: istore_1        // сохраняет результат в r
11: iinc 0, -1      // уменьшает n на 1
14: goto 2          // возвращается к проверке условия в строке 2
18: iload_1         // загружает значение r
19: ireturn         // возвращает значение r
```

**Пояснение шагов:**

1. **`iconst_1`** — Загружает константу `1` для инициализации `r`.
2. **`istore_1`** — Сохраняет значение `1` в переменную `r`.
3. **`iload_0`** — Загружает значение `n` на стек.
4. **`iconst_1`** — Загружает константу `1` на стек.
5. **`if_icmple 18`** — Проверяет, если `n <= 1`, переход к инструкции на адресе `18` (завершение цикла).
6. **`iload_1`** — Загружает текущее значение `r` на стек.
7. **`iload_0`** — Загружает текущее значение `n` на стек.
8. **`imul`** — Умножает два верхних значения на стеке (`r * n`), результат помещается на стек.
9. **`istore_1`** — Сохраняет результат умножения в `r`.
10. **`iinc 0, -1`** — Уменьшает `n` на `1`.
11. **`goto 2`** — Возвращается к началу цикла.
12. **`iload_1`** — Загружает значение `r` для возврата.
13. **`ireturn`** — Возвращает `r` как результат.

## Результат:

![image](https://github.com/user-attachments/assets/176c3e8b-234a-49b9-a4a1-f8d1cedc191c)


## Задача 4

Работа с qemu. Скачать и установить ISO-образ Alpine Linux для виртуальных машин с официального сайта.
Создать с помощью qemu образ жесткого диска (опция -f qcow2). Объем диска 500 Мб.
Запустить Alpine Linux с CD-ROM.
Установить систему на sda. Изменить motd.
Загрузиться уже с sda.
Прислать полный список команд для установки и загрузки, а также скриншот с motd, где фигурируют ваши имя и фамилия.

## Решение

```
qemu-img create -f qcow2 "C:\Program Files\qemu\images\alpine-disk.qcow2" 500M

C:\Program Files\qemu>qemu-system-x86_64 ^
 -m 512 ^
 -boot d ^
 -cdrom "C:\Program Files\qemu\iso\alpine-standard-3.20.3-x86_64.iso" ^
 -hda "C:\Program Files\qemu\images\alpine-disk.qcow2" ^
 -nic user,model=virtio-net-pci ^
 -accel tcg

setup-alpine

C:\Program Files\qemu>qemu-system-x86_64 ^
 -m 512 ^
 -boot c ^
 -hda "C:\Program Files\qemu\images\alpine-disk.qcow2" ^
 -nic user,model=virtio-net-pci ^
 -accel tcg

vi /etc/motd
(после изменений нажмите ESC, потом :wq чтобы сохранить изменений)

reboot
```
![1](https://github.com/user-attachments/assets/a6248b7a-92bb-4dde-ae6a-1408ab1f7038)

![382820147-b144b8f9-ea75-4266-9e23-ce90e6204dc8](https://github.com/user-attachments/assets/87e06ea3-1217-40fa-96c5-1a396acb0539)

## Задача 5

(после разбора на семинаре и написания у доски базовой части эмулятора древней игровой приставки CHIP-8)

1. Реализовать вывод на экран.
2. Добиться запуска Тетриса.
3. Реализовать ввод с клавиатуры.
4. Добиться успешной работы всех приложений.

## Результат

![tet1](https://github.com/user-attachments/assets/2d1e831a-b211-4e1a-8b22-dbb115ff6a4a)

![tet2](https://github.com/user-attachments/assets/0c308f14-e185-4317-8099-cdc04e772df6)

## Полезные ссылки

Compiler Explorer: https://godbolt.org/

Байткод CPython: https://docs.python.org/3/library/dis.html

QEMU для Windows: https://www.qemu.org/download/#windows
http://sovietov.com/tmp/mqemu.zip

Документация по QEMU: https://www.qemu.org/docs/master/system/index.html

Старая документация по QEMU (рус.): https://www.opennet.ru/docs/RUS/qemu_doc/

Образы Alpine Linux: https://alpinelinux.org/downloads/

Документация по игровому компьютеру CHIP-8: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

Учебник по созданию миниатюрной ОС: https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf
