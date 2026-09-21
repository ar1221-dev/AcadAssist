import { useEffect, useMemo, useRef, useState } from 'react';
import { Check, Clock3, Plus, Sparkles, Trash2, Pencil, CalendarDays } from 'lucide-react';
import HeroHeader from '../components/ui/HeroHeader';
import Modal from '../components/ui/Modal';
import { useApp, type CalendarEvent } from '../context/AppContext';

const TYPES:CalendarEvent['type'][]=['Task','Exam','Class','Assignment','Study Session','Personal Event'];
const iso=(d:Date)=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const monthDays=(year:number,month:number)=>{const first=new Date(year,month,1).getDay();const total=new Date(year,month+1,0).getDate();const cells:number[]=[];for(let i=0;i<first;i++)cells.push(0);for(let d=1;d<=total;d++)cells.push(d);while(cells.length%7)cells.push(0);return cells;};

export default function Planner(){
 const {plannerTasks,togglePlannerTask,events,addEvent,updateEvent,deleteEvent,pushToast,settings}=useApp();
 const today=new Date(); const [cursor,setCursor]=useState(new Date(today.getFullYear(),today.getMonth(),1)); const [view,setView]=useState<'Day'|'Week'|'Month'>('Month'); const [selectedDate,setSelectedDate]=useState(iso(today));
 const [taskOpen,setTaskOpen]=useState(false);const [editEvent,setEditEvent]=useState<CalendarEvent|null>(null);const [focusOpen,setFocusOpen]=useState(false);const [focusSeconds,setFocusSeconds]=useState(0);
  const [title,setTitle]=useState('');const [time,setTime]=useState('5:00 PM');const [type,setType]=useState<CalendarEvent['type']>('Task');const [subject,setSubject]=useState('');const [notes,setNotes]=useState('');
  const hadFocusRef = useRef(false);
  useEffect(()=>{
    if(focusSeconds<=0) {
      if(hadFocusRef.current) {
        hadFocusRef.current = false;
        pushToast('Focus session complete — nice work!');
      }
      return;
    }
    hadFocusRef.current = true;
    const id=window.setInterval(()=>setFocusSeconds(s=>Math.max(0,s-1)),1000);
    return()=>window.clearInterval(id);
  },[focusSeconds, pushToast]);
  const month=cursor.toLocaleString('en-US',{month:'long'});const year=cursor.getFullYear();const cells=monthDays(year,cursor.getMonth());
  const visibleEvents=useMemo(()=>{
    if(view==='Day') {
      return events.filter(e=>e.date===selectedDate).sort((a,b)=>(a.time||'').localeCompare(b.time||''));
    }
    if(view==='Month') {
      return events.filter(e=>e.date.startsWith(`${year}-${String(cursor.getMonth()+1).padStart(2,'0')}`));
    }
    const start=new Date(selectedDate+'T00:00:00');
    const day=start.getDay();
    const weekStart=new Date(start);
    weekStart.setDate(start.getDate()-day);
    const week=new Set(Array.from({length:7},(_,i)=>{const d=new Date(weekStart);d.setDate(weekStart.getDate()+i);return iso(d)}));
    return events.filter(e=>week.has(e.date));
  },[view,events,year,cursor,selectedDate]);
 const openAdd=(date=selectedDate)=>{setSelectedDate(date);setEditEvent(null);setTitle('');setTime('5:00 PM');setType('Task');setSubject('');setNotes('');setTaskOpen(true)};
 const openEdit=(e:CalendarEvent)=>{setEditEvent(e);setTitle(e.title);setTime(e.time||'');setType(e.type);setSubject(e.subject||'');setNotes(e.notes||'');setSelectedDate(e.date);setTaskOpen(true)};
 const save=()=>{if(!title.trim()){pushToast('Enter a title','error');return}const patch={date:selectedDate,title:title.trim(),time:time.trim()||undefined,type,subject:subject.trim()||undefined,notes:notes.trim()||undefined};if(editEvent){updateEvent(editEvent.id,patch);pushToast('Event updated')}else{addEvent({id:crypto.randomUUID(),...patch,completed:false});pushToast('Added to planner')}setTaskOpen(false)};
 const startFocus=(minutes:number)=>{setFocusSeconds(minutes*60);setFocusOpen(false);pushToast(`${minutes}-minute focus session started`)};
 const formatted=focusSeconds?`${String(Math.floor(focusSeconds/60)).padStart(2,'0')}:${String(focusSeconds%60).padStart(2,'0')}`:'00:00';
 return <div className="page-stack"><HeroHeader tag="STUDY PLANNER" title={<>Plan Today. Progress <span className="accent">Tomorrow.</span></>} subtitle="Schedule tasks, exams, classes and focused study sessions in one place."/>
 <div className="planner-toolbar"><div className="flex items-center gap-2"><button className="icon-button" onClick={()=>setCursor(new Date(year,cursor.getMonth()-1,1))}>‹</button><button className="btn subtle" onClick={()=>{setCursor(new Date(today.getFullYear(),today.getMonth(),1));setSelectedDate(iso(today))}}>Today</button><button className="icon-button" onClick={()=>setCursor(new Date(year,cursor.getMonth()+1,1))}>›</button><h2 className="text-lg font-bold ml-2">{month} {year}</h2></div><div className="flex gap-2"><div className="view-switch">{(['Day','Week','Month'] as const).map(v=><button key={v} onClick={()=>setView(v)} className={view===v?'active':''}>{v}</button>)}</div><button className="btn primary" onClick={()=>openAdd()}><Plus size={15}/>Add event</button></div></div>
 <div className="grid grid-cols-1 xl:grid-cols-[300px_1fr_300px] gap-6"><div><div className="card calendar-card"><div className="calendar-head"><button className="icon-button" onClick={()=>setCursor(new Date(year,cursor.getMonth()-1,1))}>‹</button><strong>{month} {year}</strong><button className="icon-button" onClick={()=>setCursor(new Date(year,cursor.getMonth()+1,1))}>›</button></div><div className="calendar-week">{['S','M','T','W','T','F','S'].map((d,i)=><span key={i}>{d}</span>)}</div><div className="calendar-days">{cells.map((d,i)=>d?<button key={i} className={`${selectedDate===`${year}-${String(cursor.getMonth()+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`?'selected ':''}${events.some(e=>e.date===`${year}-${String(cursor.getMonth()+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`)?'has-event ':''}`} onClick={()=>setSelectedDate(`${year}-${String(cursor.getMonth()+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`)}>{d}</button>:<span key={i}/>)}</div></div><div className="card p-4 mt-4"><div className="section-title-row"><h3>Study tasks</h3><span className="soft-badge">{plannerTasks.filter(t=>t.completed).length}/{plannerTasks.length}</span></div>{plannerTasks.slice(0,6).map(t=><div className="focus-item" key={t.id}><button className={`check ${t.completed?'done':''}`} onClick={()=>togglePlannerTask(t.id)}>{t.completed&&<Check size={13}/>}</button><div><b>{t.title}</b><small>{t.time} · {t.duration}</small></div></div>)}</div></div>
 <div><div className="card p-5"><div className="section-title-row"><div><div className="section-kicker">{view.toUpperCase()} VIEW</div><h2>{view==='Day'?selectedDate:view==='Week'?`Week containing ${selectedDate}`:`${month} schedule`}</h2></div><button className="btn secondary" onClick={()=>openAdd()}><Plus size={14}/>Add</button></div><div className="event-list mt-5">{visibleEvents.length?visibleEvents.map(e=><div className="event-row" key={e.id}><div className="event-time">{e.time||'All day'}</div><div className={`event-dot ${e.type.toLowerCase().replaceAll(' ','-')}`}/><button className="event-content" onClick={()=>openEdit(e)}><b className={e.completed?'line-through opacity-50':''}>{e.title}</b><small>{e.type}{e.subject?` · ${e.subject}`:''}{e.notes?` · ${e.notes}`:''}</small></button><button className="icon-button" onClick={()=>updateEvent(e.id,{completed:!e.completed})} aria-label="Toggle complete">{e.completed?<Check size={15}/>:<span>○</span>}</button><button className="icon-button" onClick={()=>deleteEvent(e.id)} aria-label="Delete"><Trash2 size={14}/></button></div>):<div className="empty-state"><CalendarDays size={28}/><h3>No events</h3><p>Add something to this part of your schedule.</p><button className="btn primary" onClick={()=>openAdd()}>Add event</button></div>}</div></div></div>
 <div><div className="card p-4"><div className="section-title-row"><div><h3>Focus mode</h3><p className="muted text-xs">Default: {settings.defaultStudyDuration} minutes</p></div><Clock3 size={18}/></div>{focusSeconds>0?<><div className="focus-timer">{formatted}</div><button className="btn secondary w-full" onClick={()=>setFocusSeconds(0)}>Stop session</button></>:<button className="btn primary w-full mt-4" onClick={()=>setFocusOpen(true)}><Sparkles size={15}/>Start focus</button>}</div><div className="card p-4 mt-4"><div className="section-kicker">AI PLANNING TIP</div><h3 className="mt-1">Prioritize what is closest to an exam.</h3><p className="muted text-xs mt-2">Use your exam dates and lower-progress subjects to decide the next study block.</p><button className="btn secondary mt-3" onClick={()=>{setSelectedDate(iso(today));setView('Day');openAdd(iso(today))}}>Schedule next block</button></div></div></div>
 <Modal open={taskOpen} onClose={()=>setTaskOpen(false)} title={editEvent?'Edit event':'Add to planner'}><div className="form-grid"><label>Title<input className="input" value={title} onChange={e=>setTitle(e.target.value)}/></label><label>Date<input className="input" type="date" value={selectedDate} onChange={e=>setSelectedDate(e.target.value)}/></label><label>Time<input className="input" value={time} onChange={e=>setTime(e.target.value)} placeholder="5:00 PM"/></label><label>Type<select className="select full" value={type} onChange={e=>setType(e.target.value as CalendarEvent['type'])}>{TYPES.map(t=><option key={t}>{t}</option>)}</select></label></div><label>Subject<input className="input" value={subject} onChange={e=>setSubject(e.target.value)}/></label><label>Notes<textarea className="textarea" rows={4} value={notes} onChange={e=>setNotes(e.target.value)}/></label><div className="modal-actions"><button className="btn secondary" onClick={()=>setTaskOpen(false)}>Cancel</button>{editEvent&&<button className="btn danger" onClick={()=>{deleteEvent(editEvent.id);setTaskOpen(false);pushToast('Event deleted','info')}}><Trash2 size={14}/>Delete</button>}<button className="btn primary" onClick={save}><Pencil size={14}/>{editEvent?'Save changes':'Add event'}</button></div></Modal>
 <Modal open={focusOpen} onClose={()=>setFocusOpen(false)} title="Start a focus session"><div className="grid grid-cols-3 gap-3">{[25,50,90].map(m=><button key={m} className="card p-4 text-center" onClick={()=>startFocus(m)}><Sparkles className="mx-auto mb-2" size={18}/><b>{m} min</b></button>)}</div><button className="btn secondary w-full mt-3" onClick={()=>{startFocus(settings.defaultStudyDuration)}}>Use my default ({settings.defaultStudyDuration} min)</button></Modal>
 </div>
}
