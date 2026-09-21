import { useEffect, useMemo, useState, type ChangeEvent } from 'react';
import { Download, Edit3, Eye, FileText, FileQuestion, MoreHorizontal, Plus, Search, Sparkles, Trash2, UploadCloud, BookOpen, Star } from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useApp, type Note } from '../context/AppContext';
import Modal from '../components/ui/Modal';
import { deleteFile, getFile, saveFile } from '../services/fileStore';

type Material = ReturnType<typeof useApp>['knowledgeMaterials'][number];

export default function Knowledge(){
 const {knowledgeMaterials,addKnowledgeMaterial,updateKnowledgeMaterial,deleteKnowledgeMaterial,notes,addNote,updateNote,deleteNote,pushToast,subjects,quizzes}=useApp();
 const [params]=useSearchParams(); const navigate=useNavigate();
 const [q,setQ]=useState(params.get('q')||''); const [tab,setTab]=useState<'Documents'|'Notes'>('Documents'); const [subject,setSubject]=useState('All'); const [type,setType]=useState('All'); const [sort,setSort]=useState('Newest');
 const [uploadOpen,setUploadOpen]=useState(false); const [file,setFile]=useState<File|null>(null); const [drag,setDrag]=useState(false); const [uploadSubject,setUploadSubject]=useState(subjects[0]?.name||''); const [actions,setActions]=useState<string|null>(null);
 const [preview,setPreview]=useState<Material|null>(null); const [previewNote,setPreviewNote]=useState<Note|null>(null); const [editDoc,setEditDoc]=useState<Material|null>(null); const [editNote,setEditNote]=useState<Note|null>(null); const [deleteTarget,setDeleteTarget]=useState<Material|null>(null);
 const [busy,setBusy]=useState(false);
 const docs=useMemo(()=>knowledgeMaterials.filter(m=>(subject==='All'||m.subject===subject)&&(type==='All'||m.type===type)&&`${m.name} ${m.subject}`.toLowerCase().includes(q.toLowerCase())).sort((a,b)=>sort==='Name'?a.name.localeCompare(b.name):new Date(b.addedOn).getTime()-new Date(a.addedOn).getTime()),[knowledgeMaterials,q,subject,type,sort]);
 const noteList=useMemo(()=>notes.filter(n=>(subject==='All'||n.subject===subject)&&`${n.title} ${n.content} ${n.source}`.toLowerCase().includes(q.toLowerCase())).sort((a,b)=>sort==='Name'?a.title.localeCompare(b.title):b.id.localeCompare(a.id)),[notes,q,subject,sort]);
 const onFile=(f:File|null)=>{if(!f)return; if(f.size>50*1024*1024){pushToast('Maximum file size is 50 MB','error');return} const ext=f.name.split('.').pop()?.toLowerCase(); if(!['pdf','docx','pptx','txt'].includes(ext||'')){pushToast('Supported formats: PDF, DOCX, PPTX and TXT','error');return} setFile(f);setUploadSubject(subjects[0]?.name||'');setUploadOpen(true)};
 const createUpload=async()=>{if(!file||!uploadSubject){pushToast('Select a subject first','error');return} setBusy(true); try{const id=crypto.randomUUID();await saveFile(id,file);const ext=file.name.split('.').pop()?.toLowerCase();const material={id,name:file.name,subject:uploadSubject,type:(ext==='pptx'?'PPT':ext?.toUpperCase()) as Material['type'],size:`${(file.size/1024/1024).toFixed(1)} MB`,addedOn:new Date().toISOString(),status:'Ready',starred:false};addKnowledgeMaterial(material); if(ext==='txt'){const text=await file.text();addNote({id:crypto.randomUUID(),title:`${file.name.replace(/\.[^.]+$/,'')} — Summary`,subject:uploadSubject,source:file.name,type:'Summary',content:text.slice(0,3500),createdAt:'Just now'});} setFile(null);setUploadOpen(false);pushToast('Material added to your Knowledge library');}catch(e){pushToast(e instanceof Error?e.message:'Could not save the file','error')}finally{setBusy(false)}};
 const download=async(m:Material)=>{try{const blob=await getFile(m.id||m.name);if(!blob)throw new Error('Original file is not available in this browser');const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=m.name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);pushToast('Download started')}catch(e){pushToast(e instanceof Error?e.message:'Download failed','error')}};
 const openPreview=async(m:Material)=>{setPreview(m);};
 const generate=(m:Material,kind:'Summary'|'AI Notes'|'Exam Notes'|'Easy Explanation')=>{const clean=m.name.replace(/\.[^.]+$/,'');const templates:{[K in typeof kind]:string}={Summary:`${clean} — concise summary\n\n• Identify the main concepts and their relationships.\n• Keep definitions, mechanisms, formulas and examples.\n• Remove repetition and low-value detail.`, 'AI Notes':`${clean} — AI notes\n\n1. Core idea\n2. Key definitions\n3. Important mechanisms / steps\n4. Examples\n5. Common exam mistakes`, 'Exam Notes':`${clean} — exam notes\n\nDefinitions → mechanisms → comparisons → formulas → likely exam questions.\n\nUse these notes as a revision outline and verify details against the source document.`, 'Easy Explanation':`${clean} — easy explanation\n\nStart with the simplest definition, explain why the concept exists, then walk through one concrete example and a common misconception.`};addNote({id:crypto.randomUUID(),title:`${clean} — ${kind}`,subject:m.subject,source:m.name,type:kind,content:templates[kind],createdAt:'Just now'});pushToast(`${kind} created`);setActions(null)};
 const removeDoc=async()=>{if(!deleteTarget)return;deleteKnowledgeMaterial(deleteTarget.id||deleteTarget.name);await deleteFile(deleteTarget.id||deleteTarget.name);setDeleteTarget(null);pushToast('Document deleted','info')};
 return <div className="page-stack"><div className="page-hero"><div><div className="eyebrow">YOUR KNOWLEDGE BASE</div><h1>Everything you study, organized.</h1><p>Store material by subject, edit its metadata, download originals, and create AI-ready notes and quizzes.</p></div><button className="btn primary" onClick={()=>setUploadOpen(true)}><UploadCloud size={16}/>Upload material</button></div>
 <div className={`upload-zone ${drag?'dragging':''}`} onDragOver={e=>{e.preventDefault();setDrag(true)}} onDragLeave={()=>setDrag(false)} onDrop={e=>{e.preventDefault();setDrag(false);onFile(e.dataTransfer.files[0])}}><UploadCloud size={28}/><h3>Drop study material here</h3><p>PDF · DOCX · PPTX · TXT · up to 50 MB</p><label className="btn secondary"><Plus size={15}/>Browse files<input hidden type="file" accept=".pdf,.docx,.pptx,.txt" onChange={(e:ChangeEvent<HTMLInputElement>)=>onFile(e.target.files?.[0]||null)}/></label></div>
 <div className="tabs-row"><button className={tab==='Documents'?'active':''} onClick={()=>setTab('Documents')}>Documents ({knowledgeMaterials.length})</button><button className={tab==='Notes'?'active':''} onClick={()=>setTab('Notes')}>AI Notes ({notes.length})</button><button onClick={()=>navigate('/assessment')}><FileQuestion size={15}/> Quizzes ({quizzes.length})</button></div>
 <div className="toolbar"><div className="search-box"><Search size={16}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search documents, notes or subjects..."/></div><select className="select" value={subject} onChange={e=>setSubject(e.target.value)}><option>All</option>{subjects.map(s=><option key={s.id}>{s.name}</option>)}</select>{tab==='Documents'&&<select className="select" value={type} onChange={e=>setType(e.target.value)}><option>All</option><option>PDF</option><option>DOCX</option><option>PPT</option><option>TXT</option></select>}<select className="select" value={sort} onChange={e=>setSort(e.target.value)}><option>Newest</option><option>Name</option></select></div>
 {tab==='Documents'?<div className="doc-grid">{docs.map(m=><div className="doc-card" key={m.id||m.name}><div className="doc-top"><div className="doc-icon"><FileText size={20}/></div><button className="icon-button" onClick={()=>setActions(actions===(m.id||m.name)?null:(m.id||m.name))}><MoreHorizontal size={18}/></button>{actions===(m.id||m.name)&&<div className="action-menu"><button onClick={()=>{openPreview(m);setActions(null)}}><Eye size={14}/>View</button><button onClick={()=>{setEditDoc(m);setActions(null)}}><Edit3 size={14}/>Edit details</button><button onClick={()=>generate(m,'Summary')}><Sparkles size={14}/>AI Summary</button><button onClick={()=>generate(m,'AI Notes')}><BookOpen size={14}/>AI Notes</button><button onClick={()=>{navigate(`/assessment?source=document&material=${encodeURIComponent(m.name)}`);setActions(null)}}><FileQuestion size={14}/>Generate Quiz</button><button onClick={()=>download(m)}><Download size={14}/>Download</button><button onClick={()=>{setDeleteTarget(m);setActions(null)}} className="danger"><Trash2 size={14}/>Delete</button></div>}</div><div className="doc-type">{m.type}</div><h3>{m.name}</h3><p>{m.subject} · {m.size}</p><div className="doc-status"><span>●</span>{m.status}</div><div className="doc-actions"><button className="btn secondary" onClick={()=>openPreview(m)}><Eye size={14}/>View</button><button className="icon-button" onClick={()=>updateKnowledgeMaterial(m.id||m.name,{starred:!m.starred})} aria-label="Star document"><Star size={15} fill={m.starred?'currentColor':'none'}/></button><button className="btn subtle" onClick={()=>generate(m,'AI Notes')}><Sparkles size={14}/>AI Notes</button></div></div>)}</div>:<div className="note-grid">{noteList.map(n=><div className="note-card" key={n.id}><div className="doc-top"><div className="note-icon"><BookOpen size={18}/></div><button className="icon-button" onClick={()=>setEditNote(n)}><Edit3 size={15}/></button></div><span className="soft-badge">{n.type}</span><h3>{n.title}</h3><p>{n.content.slice(0,220)}{n.content.length>220?'…':''}</p><small>{n.subject} · {n.source}</small><div className="doc-actions"><button className="btn secondary" onClick={()=>setPreviewNote(n)}><Eye size={14}/>Read</button><button className="btn subtle" onClick={()=>navigate(`/assessment?source=notes&material=${encodeURIComponent(n.title)}`)}><FileQuestion size={14}/>Quiz me</button><button className="icon-button danger" onClick={()=>deleteNote(n.id)}><Trash2 size={15}/></button></div></div>)}</div>}
 {((tab==='Documents'&&!docs.length)||(tab==='Notes'&&!noteList.length))&&<div className="empty-state"><Search size={28}/><h3>Nothing found</h3><p>Change your filters or add study material.</p><button className="btn primary" onClick={()=>setUploadOpen(true)}>Add material</button></div>}
 <Modal open={uploadOpen} onClose={()=>!busy&&setUploadOpen(false)} title="Add study material" subtitle="The original file is stored locally in your browser until Azure storage is connected.">{file?<><div className="file-preview"><FileText size={20}/><span><b>{file.name}</b><br/>{(file.size/1024/1024).toFixed(1)} MB</span></div><label>Subject<select className="select full" value={uploadSubject} onChange={e=>setUploadSubject(e.target.value)}>{subjects.map(s=><option key={s.id}>{s.name}</option>)}</select></label><div className="modal-actions"><button className="btn secondary" disabled={busy} onClick={()=>setFile(null)}>Choose another</button><button className="btn primary" disabled={busy} onClick={createUpload}>{busy?'Saving…':'Upload & add'}</button></div></>:<label className="big-drop"><UploadCloud size={30}/><span>Select PDF, DOCX, PPTX or TXT</span><input type="file" accept=".pdf,.docx,.pptx,.txt" onChange={e=>onFile(e.target.files?.[0]||null)}/></label>}</Modal>
 <Modal open={!!preview} onClose={()=>setPreview(null)} title={preview?.name||'Document'} subtitle={preview?`${preview.subject} · ${preview.type} · ${preview.size}`:''} wide>{preview&&<DocumentPreview material={preview}/>} {preview&&<div className="modal-actions"><button className="btn secondary" onClick={()=>download(preview)}><Download size={14}/>Download original</button><button className="btn primary" onClick={()=>{navigate(`/assessment?source=document&material=${encodeURIComponent(preview.name)}`);setPreview(null)}}><FileQuestion size={14}/>Generate quiz</button></div>}</Modal>
 <Modal open={!!previewNote} onClose={()=>setPreviewNote(null)} title={previewNote?.title||'Note'} subtitle={previewNote?`${previewNote.subject} · ${previewNote.type}`:''} wide>{previewNote&&<div className="preview-paper">{previewNote.content}</div>}</Modal>
 <Modal open={!!editDoc} onClose={()=>setEditDoc(null)} title="Edit document details"><EditDocument material={editDoc} subjects={subjects.map(s=>s.name)} onSave={(patch)=>{if(editDoc){updateKnowledgeMaterial(editDoc.id||editDoc.name,patch);setEditDoc(null);pushToast('Document details updated')}}}/></Modal>
 <Modal open={!!editNote} onClose={()=>setEditNote(null)} title="Edit note"><EditNote note={editNote} onSave={(patch)=>{if(editNote){updateNote(editNote.id,patch);setEditNote(null);pushToast('Note updated')}}}/></Modal>
 <Modal open={!!deleteTarget} onClose={()=>setDeleteTarget(null)} title="Delete document" subtitle="This removes the document from this browser's Knowledge library."><p className="text-sm">Delete <b>{deleteTarget?.name}</b>? AI notes created from it will remain available.</p><div className="modal-actions"><button className="btn secondary" onClick={()=>setDeleteTarget(null)}>Cancel</button><button className="btn danger" onClick={removeDoc}><Trash2 size={14}/>Delete</button></div></Modal>
 </div>
}

function DocumentPreview({material}:{material:Material}){
  const [url,setUrl]=useState<string|null>(null);
  const [text,setText]=useState('');
  const [error,setError]=useState('');
  useEffect(()=>{
    let active = true;
    let objectUrl:string|undefined;
    getFile(material.id||material.name).then(async blob=>{
      if(!active) return;
      if(!blob){
        setError('Original file is not available.');
        setUrl(null);
        setText('');
        return;
      }
      if(material.type==='TXT'){
        const content = await blob.text();
        if(active){
          setText(content);
          setUrl(null);
          setError('');
        }
        return;
      }
      objectUrl=URL.createObjectURL(blob);
      if(active){
        setUrl(objectUrl);
        setText('');
        setError('');
      }
    }).catch(e=>{
      if(active){
        setError(e instanceof Error?e.message:'Could not open file');
        setUrl(null);
        setText('');
      }
    });
    return()=>{
      active = false;
      if(objectUrl)URL.revokeObjectURL(objectUrl);
    };
  },[material]);
  if(error)return <div className="preview-paper">{error}</div>;
  if(text)return <pre className="preview-paper">{text}</pre>;
  if(url&&material.type==='PDF')return <iframe title={material.name} src={url} style={{width:'100%',height:520,border:0,borderRadius:12}}/>;
  return <div className="preview-paper"><b>{material.name}</b><p>This file format is stored safely for download. Browser-native editing is not reliable for DOCX/PPTX, so the metadata and AI workspace are provided here.</p><p>Use Download original to open it in its native application.</p></div>;
}

function EditDocument({material,subjects,onSave}:{material:Material|null;subjects:string[];onSave:(p:Partial<Material>)=>void}){const [name,setName]=useState(material?.name||'');const [sub,setSub]=useState(material?.subject||subjects[0]||'');return <><label>Name<input className="input" value={name} onChange={e=>setName(e.target.value)}/></label><label>Subject<select className="select full" value={sub} onChange={e=>setSub(e.target.value)}>{subjects.map(s=><option key={s}>{s}</option>)}</select></label><div className="modal-actions"><button className="btn secondary" onClick={()=>onSave({})}>Cancel</button><button className="btn primary" disabled={!name.trim()} onClick={()=>onSave({name:name.trim(),subject:sub})}><Edit3 size={14}/>Save changes</button></div></>}
function EditNote({note,onSave}:{note:Note|null;onSave:(p:Partial<Note>)=>void}){const [title,setTitle]=useState(note?.title||'');const [content,setContent]=useState(note?.content||'');return <><label>Title<input className="input" value={title} onChange={e=>setTitle(e.target.value)}/></label><label>Content<textarea className="textarea" rows={10} value={content} onChange={e=>setContent(e.target.value)}/></label><div className="modal-actions"><button className="btn primary" disabled={!title.trim()} onClick={()=>onSave({title:title.trim(),content})}>Save changes</button></div></>}
