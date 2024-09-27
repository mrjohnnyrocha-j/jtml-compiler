export function component_a2af1b0e(){let tasks_a2af1b0e=[];function addTask_a2af1b0e(task){tasks.push({task:task,completed:false});updateTaskList();}
function toggleTaskCompletion_a2af1b0e(index){tasks[index].completed=!tasks[index].completed;updateTaskList();}
function updateTaskList_a2af1b0e(){const event_a2af1b0e=new CustomEvent('tasksUpdated',{detail:tasks});querySelector_component('task-list').dispatchEvent(event);}}
component_a2af1b0e();