from devon_agent.config import Checkpoint
from devon_agent.tool import Tool, ToolContext


class AskUserTool(Tool):
    @property
    def name(self):
        return "AskUserTool"

    @property
    def supported_formats(self):
        return ["docstring", "manpage"]

    def setup(self, context: ToolContext):
        pass

    def cleanup(self, context: ToolContext):
        pass

    def documentation(self, format="docstring"):
        match format:
            case "docstring":
                return self.function.__doc__
            case "manpage":
                return """
                NAME
                    ask_user - ask the user for their input

                SYNOPSIS
                    ask_user

                DESCRIPTION
                    The ask_user command asks the user for their input

                RETURN VALUE
                    The ask_user command returns a string indicating the user's input.

                EXAMPLES
                    To ask the user for their input, run the following command:

                        ask_user
                """
            case _:
                raise ValueError(f"Invalid format: {format}")

    def function(self, context: ToolContext, question: str, **kwargs):
        """
        command_name: ask_user
        description: The ask_user command asks the user for their input
        signature: ask_user "Some question here"
        example: `ask_user "What would you like me to do?"`
        """
        return context["environment"].execute(input=question)



class AskUserToolWithCommit(Tool):
    @property
    def name(self):
        return "AskUserTool"

    @property
    def supported_formats(self):
        return ["docstring", "manpage"]

    def setup(self, context: ToolContext):
        pass

    def cleanup(self, context: ToolContext):
        pass

    def documentation(self, format="docstring"):
        match format:
            case "docstring":
                return self.function.__doc__
            case "manpage":
                return """
                NAME
                    ask_user - ask the user for their input and provide commit message for changes

                SYNOPSIS
                    ask_user "Some question here" "Some commit message here"

                DESCRIPTION
                    The ask_user command asks the user for their input

                RETURN VALUE
                    The ask_user command returns a string indicating the user's input.

                EXAMPLES
                    To ask the user for their input, run the following command:

                        ask_user "What would you like me to do?" "Added a new feature"
                """
            case _:
                raise ValueError(f"Invalid format: {format}")

    def function(self, context: ToolContext, question: str, commit_message: str, **kwargs):
        """
        command_name: ask_user
        description: The ask_user command asks the user for their input and provide a commit message for changes
        signature: ask_user "Some question here" "Some commit message here"
        example: `ask_user "What would you like me to do?" "Added a new feature"`
        """
        if commit_message:
            print("COMMIT MESSAGE: ", commit_message)
            context["event_log"].append(
                {
                    "type": "GitEvent",
                    "content": {"type": "commitRequest", "message": commit_message},
                    "producer": "",
                    "consumer": "",
                }
            )
        return context["environment"].execute(input=question)




class SetTaskTool(Tool):
    @property
    def name(self):
        return "SetTaskTool"

    @property
    def supported_formats(self):
        return ["docstring", "manpage"]

    def setup(self, context: ToolContext):
        pass

    def cleanup(self, context: ToolContext):
        pass

    def documentation(self, format="docstring"):
        match format:
            case "docstring":
                return self.function.__doc__
            case "manpage":
                return """
                NAME
                    set_task - asks the user for the task and persists it

                SYNOPSIS
                    set_task

                DESCRIPTION
                    The set_task command asks the user for their specified task

                RETURN VALUE
                    The set_task command returns a string indicating the user's input.

                EXAMPLES
                    To ask the user for their input, run the following command:

                        set_task
                """
            case _:
                raise ValueError(f"Invalid format: {format}")

    def function(self, context: ToolContext, **kwargs):
        """
        command_name: set_task
        description: The set_task command asks the user for the next task to perform
        signature: set_task
        example: `set_task`
        """
        context["session"].state.task = context["environment"].execute(
            input="what is my next task?"
        )
        return context["session"].state.task


class RespondUserTool(Tool):
    @property
    def name(self):
        return "RespondUserTool"

    def setup(self, context: ToolContext):
        pass

    def cleanup(self, context: ToolContext):
        pass

    def supported_formats(self):
        return ["docstring", "manpage"]

    def documentation(self, format="docstring"):
        match format:
            case "docstring":
                return self.function.__doc__
            case "manpage":
                return """
                NAME
                    respond - respond to the user

                SYNOPSIS
                    respond "Some response here"

                DESCRIPTION
                    The respond command responds to the user

                RETURN VALUE
                    The user may respond back to you

                EXAMPLES
                    To ask the user for their input, run the following command:

                        respond "I did this, what do you think?"
                """
            case _:
                raise ValueError(f"Invalid format: {format}")

    def function(self, context: ToolContext, response: str, **kwargs):
        """
        command_name: respond
        description: The respond command responds to the user
        signature: respond "Some response here"
        example: `respond "I did this, what do you think?"`
        """
        return context["environment"].execute(input=response)
