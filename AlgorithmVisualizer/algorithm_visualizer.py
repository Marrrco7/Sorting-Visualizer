import pygame
import random
import math

pygame.init()

class DrawInformation:


    BLACK = 250, 250, 250
    GREEN = 0, 255, 0
    RED = 255, 0, 0

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('cambria', 30)
    LARGE_FONT = pygame.font.SysFont('cambria', 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst, wallpaper_path=None):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting visualizer")
        self.set_list(lst)

        # Load the background image if a path is provided
        self.bg_image = None
        if wallpaper_path:
            self.bg_image = pygame.image.load(wallpaper_path)
            self.bg_image = pygame.transform.scale(self.bg_image, (width, height))



    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending, list_size):
    if draw_info.bg_image:
        draw_info.window.blit(draw_info.bg_image, (0, 0))
    else:
        draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'> Ascending' if ascending else '> Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset ~ SPACE - Start Sorting ~ A - Ascending ~ D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    size_text = draw_info.FONT.render(f"List Size: {list_size}", 1, draw_info.BLACK)
    draw_info.window.blit(size_text, (draw_info.width/2 - size_text.get_width()/2 , 115))

    draw_slider(draw_info, list_size)
    draw_list(draw_info)
    pygame.display.update()



def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:

        if draw_info.bg_image:
            draw_info.window.blit(draw_info.bg_image, (0, 0))
        else:
            # to change to a solid color if no image is provided
            clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                          draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
            pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()



def draw_slider(draw_info, list_size):
    slider_x = draw_info.width // 2 - 150
    slider_y = 160
    slider_width = 300
    slider_height = 10
    slider_color = (200, 200, 200)

    pygame.draw.rect(draw_info.window, slider_color, (slider_x, slider_y, slider_width, slider_height))

    handle_x = slider_x + int((list_size - 10) * slider_width / 190)  # Assuming min size is 10, max size is 200
    handle_y = slider_y - 5
    handle_width = 10
    handle_height = 20
    handle_color = (50, 50, 50)

    pygame.draw.rect(draw_info.window, handle_color, (handle_x, handle_y, handle_width, handle_height))


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst



def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst



def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst



def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge(left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged

    def recursive_merge_sort(lst, start, end):
        if end - start <= 1:
            return lst[start:end]

        mid = (start + end) // 2
        left = yield from recursive_merge_sort(lst, start, mid)
        right = yield from recursive_merge_sort(lst, mid, end)

        merged = merge(left, right)

        # Update the original list
        for i, val in enumerate(merged):
            lst[start + i] = val
            draw_list(draw_info, {start + i: draw_info.GREEN}, True)
            yield True

        return lst[start:end]

    yield from recursive_merge_sort(lst, 0, len(lst))



def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True

        return i + 1

    def recursive_quick_sort(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from recursive_quick_sort(low, pi - 1)
            yield from recursive_quick_sort(pi + 1, high)

    yield from recursive_quick_sort(0, len(lst) - 1)



def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((lst[left] > lst[largest] and ascending) or (lst[left] < lst[largest] and not ascending)):
            largest = left

        if right < n and ((lst[right] > lst[largest] and ascending) or (lst[right] < lst[largest] and not ascending)):
            largest = right

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            yield True
            yield from heapify(n, largest)

    n = len(lst)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.RED, 0: draw_info.GREEN}, True)
        yield True
        yield from heapify(i, 0)


def main():
    run = True
    clock = pygame.time.Clock()

    min_val = 0
    max_val = 100
    list_size = 50

    lst = generate_starting_list(list_size, min_val, max_val)

    # Replace 'background.jpg' with your actual image file path
    draw_info = DrawInformation(1500, 800, lst, wallpaper_path='wallpaper1.jpg')
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    dragging_slider = False

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, list_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(list_size, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_m and not sorting:
                    sorting_algorithm = merge_sort
                    sorting_algo_name = "Merge Sort"
                elif event.key == pygame.K_q and not sorting:
                    sorting_algorithm = quick_sort
                    sorting_algo_name = "Quick Sort"
                elif event.key == pygame.K_h and not sorting:
                    sorting_algorithm = heap_sort
                    sorting_algo_name = "Heap Sort"


            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                slider_x = draw_info.width // 2 - 150
                slider_y = 160


                if slider_x <= x <= slider_x + 300 and slider_y - 10 <= y <= slider_y + 10:
                    dragging_slider = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False

            if event.type == pygame.MOUSEMOTION and dragging_slider:
                x, y = pygame.mouse.get_pos()
                slider_x = draw_info.width // 2 - 150
                slider_width = 300


                list_size = max(10, min(200, int((x - slider_x) * 190 / slider_width + 10)))
                lst = generate_starting_list(list_size, min_val, max_val)
                draw_info.set_list(lst)

    pygame.quit()


if __name__ == "__main__":
    main()
