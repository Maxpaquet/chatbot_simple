## Development

### Backend - To do list

- [x] Build a mock agent making proper tool call and respecting the tool_call_id policy of OpenAI.
- [x] Build a lifespan with a checkpointer (SQLite based)
- [x] Add route `"/agent/chat/{thread_id}"` to chat with one agent
    - [ ] Add the agent id as optional param (enables later the capability to select which agent to discuss with)
    - [x] Implement pytest for the route
- [x] Add route `/agent/thread/{thread_id}` to pull the entire thread (representing the conversation) from the sqlite db.
    - [x] Implemtn pytest for the route
- [ ] Implement the logic to maintain a `profile` of the user based on previous conversation.
- [ ] Implement a test_db when mock/test variables are set to `True`

### Frontend - To do list

- [ ] Follow React typescript tutorial [here](https://handsonreact.com/docs/labs/react-tutorial-typescript#fundamentals)