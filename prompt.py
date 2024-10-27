from data_example import fulfill


class PromptFactory:
    def __init__(self):
        self.last_result_analysis_note = None
        self.last_result_with_process_raw_data = None
        self.last_process_data = None
        self.external_result_with_process_data = None
        self.external_process_data = None
        fulfill(self)

    def create_prompt(self, prompt_type):
        if prompt_type == 'propose_idea_based_on_before_prompt':
            return self.ProposeIdeaBasedOnBeforePrompt()

    def ProposeIdeaBasedOnBeforePrompt(self, msg):
        prompt = f'''
        上次实验取得的效果不够理想，希望你根据下述数据能帮我分析问题原因，提出改进方案。
        我认为上次实验的主要问题是：
        {msg}
        以下是一些外部人员测试相关实验的过程数据：
        {self.external_process_data}
        以下是一些外部人员测试相关实验的过程及对应的结果数据：
        {self.external_result_with_process_data}
        以下是我上次实验取得不良结果的过程数据：
        {self.last_process_data}
        以下是我上次实验取得不良结果的结果原始数据：
        {self.last_result_with_process_raw_data}
        以下是我查阅一些文献总结出现错误结果的一些外部其他因素：
        {self.last_result_analysis_note}
        '''
        print(prompt)
        return prompt

    def WarningBeforeExperiment(self, msg):
        prompt = f'''
        我即将开始关于{msg}的实验，请根据我实验准备过程中涉及到的过程数据，搜索相关素材，帮我分析实验的可能会有风险的实验设计。
        以下是一些外部人员测试相关实验的过程数据：
        {self.external_process_data}
        以下是一些外部人员测试相关实验的过程及对应的结果数据：
        {self.external_result_with_process_data}
        以下是我本次实验设置的过程数据：
        {self.last_process_data}
        '''
        print(prompt)
        return prompt

    def ProposeIdeaStartupPrompt(self, msg):
        return f'''
        开展实验的主要内容方向是：{msg}，帮我搜索领域知识和相关科研文献，分析实验开展的核心思路。
        '''


if __name__ == '__main__':
    prompt_factory = PromptFactory()
    prompt = prompt_factory.create_prompt('propose_idea_based_on_before_prompt')
    print(prompt)
