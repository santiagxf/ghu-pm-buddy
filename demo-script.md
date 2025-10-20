# Demo script

## Prototyping an agent

Let's use **Agent Builder** to create our first agent. Let's start with the simplest of the agents to build, the **format agent**. This agent has two tasks:

* Format the issue without changing the issue the user created.
* Apply the appropiate labels.

*AI Toolkit* is a great tool to prototype agents, it allows developers to quickly test prompts, try different models, and quickly interate during the development process.

Let's build it:

1. Go to **AI Toolkit** and go to the secction **Agents**.
2. Click on the plus sign **+**.
3. Agent Builder shows up in the screen.
4. We can give it a name so we can remember the configuration. AI Tookit automatically saves the agent configuration so we can revisit it as we iterate and improve it. In our case, let's name it *format-agent*.
5. Next, let's select the model we want to use. GitHub Models gives access to a large selection of model, from complex reasoning models to simple and fast SLMs. In our case, let's pick a general purpose model like *gpt-4.1*.
6. Now it's time to configure the instructions. 

Instructions:

```console
You are a assistant that helps with automation of tasks in GitHub repositories. You are assigned the task of formatting GitHub issues according to the following guidelines:

All issues should be properly Markdown-formatted:
* File paths and code identifiers should be enclosed in backticks
* Code blocks should be enclosed in triple backticks with the right language
* Issue titles should be concise and descriptive
            
Every issue should have at least one label. Only the following labels are allowed:
* `bug` - for bugs
* `enhancement` - for feature requests
* `question` - for questions
* `documentation` - for documentation-related tasks
            
It is IMPORTANT that you do not alter the existing content of the issue body, only the formatting. You can adjust punctuation, capitalization, or spacing/paragraphs if needed. If the issue body is already well-formatted, you should not make any changes.
```

Let's see how this works by working with a GitHub issue a user has posted:

```console
TITLE:
Improve accessibility

BODY:
hey so like the app isn’t really good for accessibility right now.
images don’t have alt text and forms are kinda bad too. for example, alt text, appropriate labels, or ARIA attributes, or keyboard navigation support.

The component FindYourTripForm.tsx has tons fo these issues

<select 
    id="collapsed-from" 
    value={from}
    onChange={(e) => setFrom(e.target.value)}
    className="w-40 p-2.5 rounded bg-white border-none text-gray-900 text-sm focus:ring-2 focus:ring-white/50 focus:outline-none"
    aria-label="Origin airport"
>

we should fix it so it works better for everyone.
also it’s probably important because people need it and there are rules about this i think.
and it makes the app nicer.
pls do something about it soon.
```

The agent outputs the right output now. As can be seen, it limited the changes to formating because we don't want to change the semantics or the actual text the user has typed.

However, to use this agent in our workflow, we would need to first retrieve the issue description, run the agent, and then run a command to update the issue. 

One of the most powerful characteristics of agents is that they can execute actions via tools. That's a great candidate for our agent because we can task our agent to use those tools to retrieve the GitHub issue and also update it once formated.

## Enhacing with MCP

The previous example works, but we would like to avoid passing directly the issue body, but to ask the agent to fetch the issue itself:

### Adding an MCP Server:

1. Go to AI Toolkit.
2. Under the section **MCP workflow**, select **Add MCP Server**.
3. You can see the list of MCP servers available in GitHub MCP registry.
4. Select **GitHub**.
5. Enter a name for the MCP server.
6. Configure authentication for the MCP server. AI Toolkit will generate an `mcp.json` file to use for configuration. By default, it's saved in the folder `/home/codespace/.aitk/mcp.json`.
7. Now, go to the section **My resources** and under **MCP Servers** you will see a new server added to the list.
8. Check the connection by right click on the new item, and select **Start**.
9. Now, in **Agent Builder**, go to the section **MCP tools** and select the plus sign, click on **MCP Server**.
10. Select GitHub from the list.
11. You have now the chance to configure which tools are available from the server to the agent. As a best practice, try to configure tools that are relevant to the task the agent has to do. This improves the chances the agent picks the right tool for the right job and doesn't get confused.
12. In our case, first click on the checkbox to deselect all the tools.
13. Since our agent has to work with issues, we can type *issue* in the description to filter for tools that are relevant to GitHub issues. Select all of them.
14. Then select **Ok** to add the tools to the agent.


### Modify the instructions

Now, it's important to instruct the agent about the use of this tools while working. We can do that by simply changing the prompt to include the instructions:

> You have access to tools that can help to query and edit issues.

The final prompt would look as follows:

```console
You are a assistant that helps with automation of tasks in GitHub repositories. You have access to tools that can help to query and edit issues. You are assigned the task of formatting GitHub issues according to the following guidelines:

All issues should be properly Markdown-formatted:
* File paths and code identifiers should be enclosed in backticks
* Code blocks should be enclosed in triple backticks with the right language
* Issue titles should be concise and descriptive
            
Every issue should have at least one label. Only the following labels are allowed:
* `bug` - for bugs
* `enhancement` - for feature requests
* `question` - for questions
* `documentation` - for documentation-related tasks
            
It is IMPORTANT that you do not alter the existing content of the issue body, only the formatting. You can adjust punctuation, capitalization, or spacing/paragraphs if needed. If the issue body is already well-formatted, you should not make any changes.

Update the issue accordingly and add the label `investigate`.
```

### Try the agent with the new instructions

Now, let's see how it changes. Instead of pasting the actual GitHub Issue description, let's input:

```console
You are assigned issue #8 at `santiagxf/travel-app`
```

We can see in the Chat 