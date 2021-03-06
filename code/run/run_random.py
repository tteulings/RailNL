import visualise as vis


def run_random(algorithm, data, times=10000, print_lines=True, map=False,
               line=False, hist=False):
    """ runs a random algorithm multiple times

    :argument algorithm:        the algorithm that is to be used, in this case of the greedy family
    :argument data:             a class with all important static information about run, such as max_duration
    :argument times:            times the algorithm is run
    :argument print_lines:      determines if lines will be printed
    :argument map:              determines if map will be printed
    :argument line:             determines if line graph will be printed
    :argument hist:             determines if histogram will be printed

    :returns best solution with the score and the generated lines.
    """

    best_solution = None

    best_solutions_scores = []
    new_solutions_scores = []

    print("generating random solution...", end='', flush=True)

    for i in range(times):
        new_solution = algorithm(data)

        if not best_solution:
            best_solution = new_solution
        elif new_solution.score > best_solution.score:
            best_solution = new_solution

        new_solutions_scores.append(new_solution.score)
        best_solutions_scores.append(best_solution.score)

    print("\t DONE")

    if print_lines:
        vis.print_results(algorithm, best_solution, data)

    if map:
        vis.draw_map(data, best_solution.lines)

    if hist:
        vis.hist(new_solutions_scores, best_solution.lines)

    if line:
        vis.plot_line(best_solutions_scores)


    return best_solution