class AIManager:
    def __init__(self):
        pass

    def recommend_files(self, usage_history):
        # File recommendaton w,th a simple frequency calculation algorithm
        file_counter = {}
        for file in usage_history:
            if file in file_counter:
                file_counter[file] += 1
            else:
                file_counter[file] = 1

        sorted_files = sorted(file_counter.items(), key=lambda x: x[1], reverse=True)
        recommendedations = [file[0] for file in sorted_files[:5]]

        return recommendedations