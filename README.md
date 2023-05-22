# Определение точек пересечения полигона и окружности

## Описание

Данный код на языке Python реализует определение точек пересечения полигона и окружности, а также проверяет, может ли круг находиться внутри полигона. 

## Зависимости

Для работы кода требуется установка следующих зависимостей:

- pygame: библиотека для создания игр и графических приложений на Python.
- aabbtree: библиотека для работы с ограничивающими объемами и пространственными деревьями AABB.

Установка зависимостей:

```shell
pip install pygame aabbtree
```

## Использование

В основной части кода вызывается функция `run(quantity)`, где `quantity` - количество объектов (полигонов и окружностей), с которыми будет производиться проверка.

Пример использования:

```python
if __name__ == '__main__':
    run(100)
```

## Параметры

В коде присутствуют следующие параметры, которые можно настроить под свои нужды:

- `frequency`: частота обновления экрана (количество кадров в секунду).
- `norm_noise`: шум для определения пересечений и ближайших точек.
- `time_predict`: время предсказания движения мыши (в секундах).
- `alg`: алгоритм проверки пересечений (может принимать значения от 1 до 4).

## Алгоритмы проверки пересечений

Код поддерживает несколько алгоритмов проверки пересечений:

1. `alg = 1`: Проверка пересечений между каждым объектом и точкой мыши.
2. `alg = 2`: Использование AABB-дерева для оптимизации проверки пересечений.
3. `alg = 3`: Предсказание движения мыши и проверка пересечений с промежуточными точками.
4. `alg = 4`: Предсказание движения мыши и определение точек пересечения с объемом и проекцией окружности.

## Графический вывод

Код использует библиотеку Pygame для графического вывода. В окне отображается полигон, окружность (положение определяется мышью) и линии, обозначающие точки пересечения или ближайшие точки объектов.

## Примечание

Прежде чем запустить код, убедитесь, что зависимости установлены правильно. После запуска программы вы можете взаимодействовать с окном Pygame с помощью мыши

 и клавиатуры.