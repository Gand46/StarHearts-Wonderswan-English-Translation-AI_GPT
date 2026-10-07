from collections import defaultdict,deque

def decode(block):
 n=int.from_bytes(block[1:3],'big');p=3;out=bytearray();flag=bits=0
 def bit():
  nonlocal flag,bits,p
  if not bits:flag=block[p];p+=1;bits=8
  v=flag&1;flag>>=1;bits-=1;return v
 for _ in range(n):
  if not bit():out.append(block[p]);p+=1
  elif not bit():
   size=block[p]+11;p+=1;out.extend(block[p:p+size]);p+=size
  else:
   word=int.from_bytes(block[p:p+2],'little');p+=2;dist=(word&0xfff)+1;size=(word>>12)&15
   if not size:size=block[p]+16;p+=1
   size+=2
   for _ in range(size):out.append(out[-dist])
 return bytes(out),p

def encode(target):
 idx=defaultdict(lambda:deque(maxlen=128));out=bytearray(b'\0\0\0');bitidx=8;flagloc=-1;nt=0
 def bit(v):
  nonlocal bitidx,flagloc
  if bitidx==8:flagloc=len(out);out.append(0);bitidx=0
  out[flagloc]|=v<<bitidx;bitidx+=1
 def add(start,size):
  for k in range(start,start+size):
   if k+3<=len(target):idx[target[k:k+3]].append(k)
 def best(pos):
  if pos+3>len(target):return (0,0)
  ps=idx.get(target[pos:pos+3],());bestlen=0;distance=0
  for old in reversed(ps):
   d=pos-old
   if d>4096:break
   n=3;limit=min(273,len(target)-pos)
   while n<limit and target[pos+n]==target[pos+n-d]:n+=1
   if n>bestlen:bestlen=n;distance=d
   if n==273:break
  return bestlen,distance
 i=0
 while i<len(target):
  length,d=best(i)
  if length>=3:
   bit(1);bit(1);v=length-2
   if length>=18:v=0
   out.extend(((v<<12)|(d-1)).to_bytes(2,'little'))
   if length>=18:out.append(length-18)
   n=length
  else:
   j=i+1
   while j<min(i+266,len(target)) and best(j)[0]<3:j+=1
   if j-i>=11:
    bit(1);bit(0);out.append(j-i-11);out.extend(target[i:j]);n=j-i
   else:
    bit(0);out.append(target[i]);n=1
  nt+=1;add(i,n);i+=n
 assert nt<65536
 out[1:3]=nt.to_bytes(2,'big')
 assert decode(out)[0]==target,(len(out),nt)
 return bytes(out)

