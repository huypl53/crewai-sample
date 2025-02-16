from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

search_tool = SerperDevTool()


@CrewBase
class CrewInterview:
    """CrewInterview crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            llm=LLM(model=os.getenv("MODEL"), api_key=os.getenv("GEMINI_API_KEY")),
            # llm="gemini/gemini-1.5-flash",
            config=self.agents_config["researcher"],
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            llm=LLM(model=os.getenv("MODEL"), api_key=os.getenv("GEMINI_API_KEY")),
            # llm=LLM(model="gemini-1.5-flash"),
            # llm="gemini/gemini-1.5-flash",
            config=self.agents_config["writer"],
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            cache=False,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"], human_input=True)

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config["writing_task"], human_input=True)
        # , output_file="report.md")

    @crew
    def crew(self) -> Crew:
        """Creates the CrewInterview crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            # memory=True,
            planning=True,  # Enable planning feature for the crew
            # Embedder configuration when using memory
            embedder={
                "provider": "google",
                "config": {
                    "api_key": os.getenv("GEMINI_API_KEY"),
                    "model": os.getenv("MODEL"),
                },
            },
            planning_llm=LLM(
                model=os.getenv("MODEL"), api_key=os.getenv("GEMINI_API_KEY")
            ),
        )
