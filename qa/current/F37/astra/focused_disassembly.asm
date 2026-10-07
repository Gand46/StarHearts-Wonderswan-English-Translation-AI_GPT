
ROM 3A2530..3A25EE

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a2530 <.data>:
  3a2530:	50                   	push   ax
  3a2531:	53                   	push   bx
  3a2532:	8b d9                	mov    bx,cx
  3a2534:	d1 e3                	shl    bx,1
  3a2536:	26 8b 40 02          	mov    ax,WORD PTR es:[bx+si+0x2]
  3a253a:	26 8b 1c             	mov    bx,WORD PTR es:[si]
  3a253d:	83 c6 02             	add    si,0x2
  3a2540:	c1 e0 03             	shl    ax,0x3
  3a2543:	d1 e3                	shl    bx,1
  3a2545:	03 f0                	add    si,ax
  3a2547:	03 f3                	add    si,bx
  3a2549:	5b                   	pop    bx
  3a254a:	58                   	pop    ax
  3a254b:	cb                   	retf
  3a254c:	50                   	push   ax
  3a254d:	53                   	push   bx
  3a254e:	51                   	push   cx
  3a254f:	52                   	push   dx
  3a2550:	56                   	push   si
  3a2551:	55                   	push   bp
  3a2552:	8c d8                	mov    ax,ds
  3a2554:	8c c3                	mov    bx,es
  3a2556:	8e db                	mov    ds,bx
  3a2558:	8e c0                	mov    es,ax
  3a255a:	8a 64 01             	mov    ah,BYTE PTR [si+0x1]
  3a255d:	8a 44 02             	mov    al,BYTE PTR [si+0x2]
  3a2560:	3b c8                	cmp    cx,ax
  3a2562:	73 7a                	jae    0x3a25de
  3a2564:	6b d9 03             	imul   bx,cx,0x3
  3a2567:	03 de                	add    bx,si
  3a2569:	8a 67 04             	mov    ah,BYTE PTR [bx+0x4]
  3a256c:	8a 47 05             	mov    al,BYTE PTR [bx+0x5]
  3a256f:	3d 00 00             	cmp    ax,0x0
  3a2572:	74 6a                	je     0x3a25de
  3a2574:	03 f0                	add    si,ax
  3a2576:	8a 64 01             	mov    ah,BYTE PTR [si+0x1]
  3a2579:	8a 44 02             	mov    al,BYTE PTR [si+0x2]
  3a257c:	8b e8                	mov    bp,ax
  3a257e:	83 c6 03             	add    si,0x3
  3a2581:	fc                   	cld
  3a2582:	ba 00 00             	mov    dx,0x0
  3a2585:	45                   	inc    bp
  3a2586:	4d                   	dec    bp
  3a2587:	74 55                	je     0x3a25de
  3a2589:	d1 ea                	shr    dx,1
  3a258b:	84 f6                	test   dh,dh
  3a258d:	75 05                	jne    0x3a2594
  3a258f:	8a 14                	mov    dl,BYTE PTR [si]
  3a2591:	fe ce                	dec    dh
  3a2593:	46                   	inc    si
  3a2594:	f6 c2 01             	test   dl,0x1
  3a2597:	75 03                	jne    0x3a259c
  3a2599:	a4                   	movs   BYTE PTR es:[di],BYTE PTR ds:[si]
  3a259a:	eb ea                	jmp    0x3a2586
  3a259c:	d1 ea                	shr    dx,1
  3a259e:	84 f6                	test   dh,dh
  3a25a0:	75 06                	jne    0x3a25a8
  3a25a2:	8a 14                	mov    dl,BYTE PTR [si]
  3a25a4:	fe ce                	dec    dh
  3a25a6:	46                   	inc    si
  3a25a7:	90                   	nop
  3a25a8:	f6 c2 01             	test   dl,0x1
  3a25ab:	74 25                	je     0x3a25d2
  3a25ad:	8b df                	mov    bx,di
  3a25af:	ad                   	lods   ax,WORD PTR ds:[si]
  3a25b0:	b5 00                	mov    ch,0x0
  3a25b2:	8a cc                	mov    cl,ah
  3a25b4:	25 ff 0f             	and    ax,0xfff
  3a25b7:	40                   	inc    ax
  3a25b8:	2b d8                	sub    bx,ax
  3a25ba:	c1 e9 04             	shr    cx,0x4
  3a25bd:	75 07                	jne    0x3a25c6
  3a25bf:	8a 0c                	mov    cl,BYTE PTR [si]
  3a25c1:	46                   	inc    si
  3a25c2:	83 c1 10             	add    cx,0x10
  3a25c5:	90                   	nop
  3a25c6:	83 c1 02             	add    cx,0x2
  3a25c9:	56                   	push   si
  3a25ca:	8b f3                	mov    si,bx
  3a25cc:	f3 26 a4             	rep movs BYTE PTR es:[di],BYTE PTR es:[si]
  3a25cf:	5e                   	pop    si
  3a25d0:	eb b4                	jmp    0x3a2586
  3a25d2:	b5 00                	mov    ch,0x0
  3a25d4:	8a 0c                	mov    cl,BYTE PTR [si]
  3a25d6:	46                   	inc    si
  3a25d7:	83 c1 0b             	add    cx,0xb
  3a25da:	f3 a4                	rep movs BYTE PTR es:[di],BYTE PTR ds:[si]
  3a25dc:	eb a8                	jmp    0x3a2586
  3a25de:	8c d8                	mov    ax,ds
  3a25e0:	8c c3                	mov    bx,es
  3a25e2:	8e db                	mov    ds,bx
  3a25e4:	8e c0                	mov    es,ax
  3a25e6:	5d                   	pop    bp
  3a25e7:	5e                   	pop    si
  3a25e8:	5a                   	pop    dx
  3a25e9:	59                   	pop    cx
  3a25ea:	5b                   	pop    bx
  3a25eb:	58                   	pop    ax
  3a25ec:	cb                   	retf
  3a25ed:	90                   	nop

ROM 3A94F0..3A9594

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a94f0 <.data>:
  3a94f0:	50                   	push   ax
  3a94f1:	53                   	push   bx
  3a94f2:	51                   	push   cx
  3a94f3:	52                   	push   dx
  3a94f4:	1e                   	push   ds
  3a94f5:	06                   	push   es
  3a94f6:	56                   	push   si
  3a94f7:	57                   	push   di
  3a94f8:	55                   	push   bp
  3a94f9:	2e c5 2e 88 95       	lds    bp,DWORD PTR cs:0x9588
  3a94fe:	d1 e0                	shl    ax,1
  3a9500:	03 e8                	add    bp,ax
  3a9502:	3e 8b 6e 00          	mov    bp,WORD PTR ds:[bp+0x0]
  3a9506:	50                   	push   ax
  3a9507:	b0 f0                	mov    al,0xf0
  3a9509:	e6 c2                	out    0xc2,al
  3a950b:	58                   	pop    ax
  3a950c:	3e 8b 4e 00          	mov    cx,WORD PTR ds:[bp+0x0]
  3a9510:	83 c5 02             	add    bp,0x2
  3a9513:	2e c4 36 8c 95       	les    si,DWORD PTR cs:0x958c
  3a9518:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a951d:	90                   	nop
  3a951e:	2e 8e 1e 8a 95       	mov    ds,WORD PTR cs:0x958a
  3a9523:	3e 8b 4e 00          	mov    cx,WORD PTR ds:[bp+0x0]
  3a9527:	83 c5 02             	add    bp,0x2
  3a952a:	83 f9 ff             	cmp    cx,0xffff
  3a952d:	74 13                	je     0x3a9542
  3a952f:	3e 8b 7e 00          	mov    di,WORD PTR ds:[bp+0x0]
  3a9533:	83 c5 02             	add    bp,0x2
  3a9536:	2e 8e 1e 92 95       	mov    ds,WORD PTR cs:0x9592
  3a953b:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a9540:	eb dc                	jmp    0x3a951e
  3a9542:	2e 8e 1e 8a 95       	mov    ds,WORD PTR cs:0x958a
  3a9547:	3e 8b 7e 00          	mov    di,WORD PTR ds:[bp+0x0]
  3a954b:	83 c5 02             	add    bp,0x2
  3a954e:	83 ff ff             	cmp    di,0xffff
  3a9551:	74 2b                	je     0x3a957e
  3a9553:	2e c4 36 8c 95       	les    si,DWORD PTR cs:0x958c
  3a9558:	b9 00 00             	mov    cx,0x0
  3a955b:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a9560:	2e 8e 1e 8a 95       	mov    ds,WORD PTR cs:0x958a
  3a9565:	3e 8b 4e 00          	mov    cx,WORD PTR ds:[bp+0x0]
  3a9569:	83 c5 02             	add    bp,0x2
  3a956c:	83 f9 ff             	cmp    cx,0xffff
  3a956f:	74 0d                	je     0x3a957e
  3a9571:	2e 8e 1e 92 95       	mov    ds,WORD PTR cs:0x9592
  3a9576:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a957b:	eb e3                	jmp    0x3a9560
  3a957d:	90                   	nop
  3a957e:	5d                   	pop    bp
  3a957f:	5f                   	pop    di
  3a9580:	5e                   	pop    si
  3a9581:	07                   	pop    es
  3a9582:	1f                   	pop    ds
  3a9583:	5a                   	pop    dx
  3a9584:	59                   	pop    cx
  3a9585:	5b                   	pop    bx
  3a9586:	58                   	pop    ax
  3a9587:	c3                   	ret
  3a9588:	94                   	xchg   sp,ax
  3a9589:	5f                   	pop    di
  3a958a:	00 60 1c             	add    BYTE PTR [bx+si+0x1c],ah
  3a958d:	84 00                	test   BYTE PTR [bx+si],al
  3a958f:	20 00                	and    BYTE PTR [bx+si],al
  3a9591:	00 00                	add    BYTE PTR [bx+si],al
	...

ROM 3A3604..3A3642

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a3604 <.data>:
  3a3604:	50                   	push   ax
  3a3605:	b0 f0                	mov    al,0xf0
  3a3607:	e6 c2                	out    0xc2,al
  3a3609:	58                   	pop    ax
  3a360a:	2e c4 36 3e 36       	les    si,DWORD PTR cs:0x363e
  3a360f:	b9 00 00             	mov    cx,0x0
  3a3612:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a3617:	bf 20 40             	mov    di,0x4020
  3a361a:	b9 00 00             	mov    cx,0x0
  3a361d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3622:	b9 02 00             	mov    cx,0x2
  3a3625:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a362a:	b9 03 00             	mov    cx,0x3
  3a362d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3632:	bf 00 30             	mov    di,0x3000
  3a3635:	b9 01 00             	mov    cx,0x1
  3a3638:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a363d:	c3                   	ret
  3a363e:	1c 84                	sbb    al,0x84
  3a3640:	00 20                	add    BYTE PTR [bx+si],ah

ROM 3A3C34..3A3C72

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a3c34 <.data>:
  3a3c34:	50                   	push   ax
  3a3c35:	b0 f0                	mov    al,0xf0
  3a3c37:	e6 c2                	out    0xc2,al
  3a3c39:	58                   	pop    ax
  3a3c3a:	2e c4 36 6e 3c       	les    si,DWORD PTR cs:0x3c6e
  3a3c3f:	b9 00 00             	mov    cx,0x0
  3a3c42:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a3c47:	bf 20 40             	mov    di,0x4020
  3a3c4a:	b9 00 00             	mov    cx,0x0
  3a3c4d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3c52:	b9 02 00             	mov    cx,0x2
  3a3c55:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3c5a:	b9 03 00             	mov    cx,0x3
  3a3c5d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3c62:	bf 00 30             	mov    di,0x3000
  3a3c65:	b9 01 00             	mov    cx,0x1
  3a3c68:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3c6d:	c3                   	ret
  3a3c6e:	1c 84                	sbb    al,0x84
  3a3c70:	00 20                	add    BYTE PTR [bx+si],ah

ROM 3A9C8E..3A9CCC

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a9c8e <.data>:
  3a9c8e:	50                   	push   ax
  3a9c8f:	b0 f0                	mov    al,0xf0
  3a9c91:	e6 c2                	out    0xc2,al
  3a9c93:	58                   	pop    ax
  3a9c94:	2e c4 36 c8 9c       	les    si,DWORD PTR cs:0x9cc8
  3a9c99:	b9 00 00             	mov    cx,0x0
  3a9c9c:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a9ca1:	bf 20 40             	mov    di,0x4020
  3a9ca4:	b9 00 00             	mov    cx,0x0
  3a9ca7:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a9cac:	b9 02 00             	mov    cx,0x2
  3a9caf:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a9cb4:	b9 03 00             	mov    cx,0x3
  3a9cb7:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a9cbc:	bf 00 30             	mov    di,0x3000
  3a9cbf:	b9 01 00             	mov    cx,0x1
  3a9cc2:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a9cc7:	c3                   	ret
  3a9cc8:	1c 84                	sbb    al,0x84
  3a9cca:	00 20                	add    BYTE PTR [bx+si],ah

ROM 3AA0A4..3AA0E2

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003aa0a4 <.data>:
  3aa0a4:	50                   	push   ax
  3aa0a5:	b0 f0                	mov    al,0xf0
  3aa0a7:	e6 c2                	out    0xc2,al
  3aa0a9:	58                   	pop    ax
  3aa0aa:	2e c4 36 de a0       	les    si,DWORD PTR cs:0xa0de
  3aa0af:	b9 00 00             	mov    cx,0x0
  3aa0b2:	9a 30 25 00 a0       	call   0xa000:0x2530
  3aa0b7:	bf 20 40             	mov    di,0x4020
  3aa0ba:	b9 00 00             	mov    cx,0x0
  3aa0bd:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa0c2:	b9 02 00             	mov    cx,0x2
  3aa0c5:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa0ca:	b9 03 00             	mov    cx,0x3
  3aa0cd:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa0d2:	bf 00 30             	mov    di,0x3000
  3aa0d5:	b9 01 00             	mov    cx,0x1
  3aa0d8:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa0dd:	c3                   	ret
  3aa0de:	1c 84                	sbb    al,0x84
  3aa0e0:	00 20                	add    BYTE PTR [bx+si],ah

ROM 3AA634..3AA672

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003aa634 <.data>:
  3aa634:	50                   	push   ax
  3aa635:	b0 f0                	mov    al,0xf0
  3aa637:	e6 c2                	out    0xc2,al
  3aa639:	58                   	pop    ax
  3aa63a:	2e c4 36 6e a6       	les    si,DWORD PTR cs:0xa66e
  3aa63f:	b9 00 00             	mov    cx,0x0
  3aa642:	9a 30 25 00 a0       	call   0xa000:0x2530
  3aa647:	bf 20 40             	mov    di,0x4020
  3aa64a:	b9 00 00             	mov    cx,0x0
  3aa64d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa652:	b9 02 00             	mov    cx,0x2
  3aa655:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa65a:	b9 03 00             	mov    cx,0x3
  3aa65d:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa662:	bf 00 30             	mov    di,0x3000
  3aa665:	b9 01 00             	mov    cx,0x1
  3aa668:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa66d:	c3                   	ret
  3aa66e:	1c 84                	sbb    al,0x84
  3aa670:	00 20                	add    BYTE PTR [bx+si],ah

ROM 3A8D06..3A8D54

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a8d06 <.data>:
  3a8d06:	b8 01 00             	mov    ax,0x1
  3a8d09:	e7 00                	out    0x0,ax
  3a8d0b:	b8 0b 00             	mov    ax,0xb
  3a8d0e:	e8 df 07             	call   0x3a94f0
  3a8d11:	50                   	push   ax
  3a8d12:	b0 f0                	mov    al,0xf0
  3a8d14:	e6 c2                	out    0xc2,al
  3a8d16:	58                   	pop    ax
  3a8d17:	2e c4 36 50 8d       	les    si,DWORD PTR cs:0x8d50
  3a8d1c:	b9 0c 00             	mov    cx,0xc
  3a8d1f:	9a 30 25 00 a0       	call   0xa000:0x2530
  3a8d24:	8b 0e 2f d1          	mov    cx,WORD PTR ds:0xd12f
  3a8d28:	83 e9 01             	sub    cx,0x1
  3a8d2b:	bf c0 49             	mov    di,0x49c0
  3a8d2e:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a8d33:	53                   	push   bx
  3a8d34:	52                   	push   dx
  3a8d35:	57                   	push   di
  3a8d36:	bf 00 38             	mov    di,0x3800
  3a8d39:	bb 12 1c             	mov    bx,0x1c12
  3a8d3c:	ba 00 30             	mov    dx,0x3000
  3a8d3f:	9a b0 b8 00 a0       	call   0xa000:0xb8b0
  3a8d44:	5f                   	pop    di
  3a8d45:	5a                   	pop    dx
  3a8d46:	5b                   	pop    bx
  3a8d47:	e8 0a 00             	call   0x3a8d54
  3a8d4a:	b8 07 00             	mov    ax,0x7
  3a8d4d:	e7 00                	out    0x0,ax
  3a8d4f:	c3                   	ret
  3a8d50:	1c 84                	sbb    al,0x84
  3a8d52:	00 20                	add    BYTE PTR [bx+si],ah

ROM 340268..34031A

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

00340268 <.data>:
  340268:	50                   	push   ax
  340269:	53                   	push   bx
  34026a:	51                   	push   cx
  34026b:	52                   	push   dx
  34026c:	06                   	push   es
  34026d:	56                   	push   si
  34026e:	57                   	push   di
  34026f:	83 3e 1b eb 00       	cmp    WORD PTR ds:0xeb1b,0x0
  340274:	75 28                	jne    0x34029e
  340276:	b9 00 00             	mov    cx,0x0
  340279:	bb 00 00             	mov    bx,0x0
  34027c:	a1 cf e9             	mov    ax,ds:0xe9cf
  34027f:	8b 36 c9 e9          	mov    si,WORD PTR ds:0xe9c9
  340283:	c1 e6 05             	shl    si,0x5
  340286:	eb 10                	jmp    0x340298
  340288:	89 87 d3 e9          	mov    WORD PTR [bx-0x162d],ax
  34028c:	2e 03 84 c5 04       	add    ax,WORD PTR cs:[si+0x4c5]
  340291:	83 c6 02             	add    si,0x2
  340294:	41                   	inc    cx
  340295:	83 c3 02             	add    bx,0x2
  340298:	3b 0e d1 e9          	cmp    cx,WORD PTR ds:0xe9d1
  34029c:	72 ea                	jb     0x340288
  34029e:	50                   	push   ax
  34029f:	b0 ef                	mov    al,0xef
  3402a1:	e6 c2                	out    0xc2,al
  3402a3:	58                   	pop    ax
  3402a4:	8b 36 c9 e9          	mov    si,WORD PTR ds:0xe9c9
  3402a8:	c1 e6 03             	shl    si,0x3
  3402ab:	2e c4 84 f5 03       	les    ax,DWORD PTR cs:[si+0x3f5]
  3402b0:	8b f0                	mov    si,ax
  3402b2:	b9 00 00             	mov    cx,0x0
  3402b5:	9a ee 25 00 a0       	call   0xa000:0x25ee
  3402ba:	8b 3e cf e9          	mov    di,WORD PTR ds:0xe9cf
  3402be:	c1 e7 05             	shl    di,0x5
  3402c1:	81 c7 00 40          	add    di,0x4000
  3402c5:	b9 00 00             	mov    cx,0x0
  3402c8:	eb 06                	jmp    0x3402d0
  3402ca:	9a 18 26 00 a0       	call   0xa000:0x2618
  3402cf:	41                   	inc    cx
  3402d0:	3b 0e d1 e9          	cmp    cx,WORD PTR ds:0xe9d1
  3402d4:	72 f4                	jb     0x3402ca
  3402d6:	e8 41 00             	call   0x34031a
  3402d9:	8b 36 c9 e9          	mov    si,WORD PTR ds:0xe9c9
  3402dd:	c1 e6 03             	shl    si,0x3
  3402e0:	2e c4 84 f9 03       	les    ax,DWORD PTR cs:[si+0x3f9]
  3402e5:	8b f0                	mov    si,ax
  3402e7:	bf 42 ff             	mov    di,0xff42
  3402ea:	8b 1e c9 e9          	mov    bx,WORD PTR ds:0xe9c9
  3402ee:	d1 e3                	shl    bx,1
  3402f0:	2e 8b 8f 6d 08       	mov    cx,WORD PTR cs:[bx+0x86d]
  3402f5:	90                   	nop
  3402f6:	b5 07                	mov    ch,0x7
  3402f8:	57                   	push   di
  3402f9:	90                   	nop
  3402fa:	26 8b 04             	mov    ax,WORD PTR es:[si]
  3402fd:	83 c6 02             	add    si,0x2
  340300:	89 05                	mov    WORD PTR [di],ax
  340302:	83 c7 02             	add    di,0x2
  340305:	fe cd                	dec    ch
  340307:	75 f1                	jne    0x3402fa
  340309:	5f                   	pop    di
  34030a:	83 c7 20             	add    di,0x20
  34030d:	fe c9                	dec    cl
  34030f:	75 e5                	jne    0x3402f6
  340311:	5f                   	pop    di
  340312:	5e                   	pop    si
  340313:	07                   	pop    es
  340314:	5a                   	pop    dx
  340315:	59                   	pop    cx
  340316:	5b                   	pop    bx
  340317:	58                   	pop    ax
  340318:	c3                   	ret
  340319:	90                   	nop

ROM 396504..396550

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

00396504 <.data>:
  396504:	50                   	push   ax
  396505:	51                   	push   cx
  396506:	06                   	push   es
  396507:	56                   	push   si
  396508:	57                   	push   di
  396509:	50                   	push   ax
  39650a:	b0 ca                	mov    al,0xca
  39650c:	e6 c2                	out    0xc2,al
  39650e:	58                   	pop    ax
  39650f:	2e c4 36 4a 65       	les    si,DWORD PTR cs:0x654a
  396514:	8b 0e e9 ca          	mov    cx,WORD PTR ds:0xcae9
  396518:	bf 00 80             	mov    di,0x8000
  39651b:	9a 18 26 00 a0       	call   0xa000:0x2618
  396520:	50                   	push   ax
  396521:	b0 cd                	mov    al,0xcd
  396523:	e6 c2                	out    0xc2,al
  396525:	58                   	pop    ax
  396526:	a1 eb ca             	mov    ax,ds:0xcaeb
  396529:	c1 e0 08             	shl    ax,0x8
  39652c:	05 cc 5d             	add    ax,0x5dcc
  39652f:	e7 40                	out    0x40,ax
  396531:	b8 02 00             	mov    ax,0x2
  396534:	e7 42                	out    0x42,ax
  396536:	b8 00 fe             	mov    ax,0xfe00
  396539:	e7 44                	out    0x44,ax
  39653b:	b8 00 01             	mov    ax,0x100
  39653e:	e7 46                	out    0x46,ax
  396540:	b0 80                	mov    al,0x80
  396542:	e6 48                	out    0x48,al
  396544:	5f                   	pop    di
  396545:	5e                   	pop    si
  396546:	07                   	pop    es
  396547:	59                   	pop    cx
  396548:	58                   	pop    ax
  396549:	cb                   	retf
  39654a:	00 00                	add    BYTE PTR [bx+si],al
  39654c:	00 20                	add    BYTE PTR [bx+si],ah
  39654e:	50                   	push   ax
  39654f:	53                   	push   bx

ROM 3A3634..3A364D

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a3634 <.data>:
  3a3634:	30 b9 01 00          	xor    BYTE PTR [bx+di+0x1],bh
  3a3638:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a363d:	c3                   	ret
  3a363e:	1c 84                	sbb    al,0x84
  3a3640:	00 20                	add    BYTE PTR [bx+si],ah
  3a3642:	b8 01 00             	mov    ax,0x1
  3a3645:	e7 00                	out    0x0,ax
  3a3647:	b8 0f 00             	mov    ax,0xf
  3a364a:	e8 a3 5e             	call   0x3a94f0

ROM 3A3C64..3A3C7D

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a3c64 <.data>:
  3a3c64:	30 b9 01 00          	xor    BYTE PTR [bx+di+0x1],bh
  3a3c68:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3a3c6d:	c3                   	ret
  3a3c6e:	1c 84                	sbb    al,0x84
  3a3c70:	00 20                	add    BYTE PTR [bx+si],ah
  3a3c72:	b8 01 00             	mov    ax,0x1
  3a3c75:	e7 00                	out    0x0,ax
  3a3c77:	b8 0e 00             	mov    ax,0xe
  3a3c7a:	e8 73 58             	call   0x3a94f0

ROM 3A473E..3A4757

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a473e <.data>:
  3a473e:	01 e8                	add    ax,bp
  3a4740:	ac                   	lods   al,BYTE PTR ds:[si]
  3a4741:	00 c6                	add    dh,al
  3a4743:	06                   	push   es
  3a4744:	8d                   	lea    cx,(bad)
  3a4745:	ca 01 eb             	retf   0xeb01
  3a4748:	a5                   	movs   WORD PTR es:[di],WORD PTR ds:[si]
  3a4749:	90                   	nop
  3a474a:	c3                   	ret
  3a474b:	90                   	nop
  3a474c:	b8 01 00             	mov    ax,0x1
  3a474f:	e7 00                	out    0x0,ax
  3a4751:	b8 00 00             	mov    ax,0x0
  3a4754:	e8 99 4d             	call   0x3a94f0

ROM 3A4C6E..3A4C87

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a4c6e <.data>:
  3a4c6e:	00 e8                	add    al,ch
  3a4c70:	54                   	push   sp
  3a4c71:	00 c6                	add    dh,al
  3a4c73:	06                   	push   es
  3a4c74:	8d                   	lea    cx,(bad)
  3a4c75:	ca 01 eb             	retf   0xeb01
  3a4c78:	a5                   	movs   WORD PTR es:[di],WORD PTR ds:[si]
  3a4c79:	90                   	nop
  3a4c7a:	c3                   	ret
  3a4c7b:	90                   	nop
  3a4c7c:	b8 01 00             	mov    ax,0x1
  3a4c7f:	e7 00                	out    0x0,ax
  3a4c81:	b8 01 00             	mov    ax,0x1
  3a4c84:	e8 69 48             	call   0x3a94f0

ROM 3A5140..3A5159

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a5140 <.data>:
  3a5140:	e8 2b 01             	call   0x3a526e
  3a5143:	c3                   	ret
  3a5144:	b8 01 00             	mov    ax,0x1
  3a5147:	e7 00                	out    0x0,ax
  3a5149:	b8 02 00             	mov    ax,0x2
  3a514c:	80 3e 04 c0 00       	cmp    BYTE PTR ds:0xc004,0x0
  3a5151:	74 03                	je     0x3a5156
  3a5153:	b8 11 00             	mov    ax,0x11
  3a5156:	e8 97 43             	call   0x3a94f0

ROM 3A5F9C..3A5FB5

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a5f9c <.data>:
  3a5f9c:	33 d2                	xor    dx,dx
  3a5f9e:	bb 0a 00             	mov    bx,0xa
  3a5fa1:	f7 f3                	div    bx
  3a5fa3:	88 16 9a ca          	mov    BYTE PTR ds:0xca9a,dl
  3a5fa7:	90                   	nop
  3a5fa8:	c3                   	ret
  3a5fa9:	90                   	nop
  3a5faa:	b8 01 00             	mov    ax,0x1
  3a5fad:	e7 00                	out    0x0,ax
  3a5faf:	b8 03 00             	mov    ax,0x3
  3a5fb2:	e8 3b 35             	call   0x3a94f0

ROM 3A672A..3A6743

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a672a <.data>:
  3a672a:	e8 2d 01             	call   0x3a685a
  3a672d:	c3                   	ret
  3a672e:	b8 01 00             	mov    ax,0x1
  3a6731:	e7 00                	out    0x0,ax
  3a6733:	b8 04 00             	mov    ax,0x4
  3a6736:	80 3e 04 c0 00       	cmp    BYTE PTR ds:0xc004,0x0
  3a673b:	74 03                	je     0x3a6740
  3a673d:	b8 12 00             	mov    ax,0x12
  3a6740:	e8 ad 2d             	call   0x3a94f0

ROM 3A7478..3A7491

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a7478 <.data>:
  3a7478:	02 e8                	add    ch,al
  3a747a:	c2 02 72             	ret    0x7202
  3a747d:	06                   	push   es
  3a747e:	e8 a1 cf             	call   0x3a4422
  3a7481:	73 eb                	jae    0x3a746e
  3a7483:	90                   	nop
  3a7484:	c3                   	ret
  3a7485:	90                   	nop
  3a7486:	b8 01 00             	mov    ax,0x1
  3a7489:	e7 00                	out    0x0,ax
  3a748b:	b8 05 00             	mov    ax,0x5
  3a748e:	e8 5f 20             	call   0x3a94f0

ROM 3A792A..3A7943

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a792a <.data>:
  3a792a:	33 d2                	xor    dx,dx
  3a792c:	bb 0a 00             	mov    bx,0xa
  3a792f:	f7 f3                	div    bx
  3a7931:	88 16 a0 ca          	mov    BYTE PTR ds:0xcaa0,dl
  3a7935:	90                   	nop
  3a7936:	c3                   	ret
  3a7937:	90                   	nop
  3a7938:	b8 01 00             	mov    ax,0x1
  3a793b:	e7 00                	out    0x0,ax
  3a793d:	b8 06 00             	mov    ax,0x6
  3a7940:	e8 ad 1b             	call   0x3a94f0

ROM 3A7EF8..3A7F11

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a7ef8 <.data>:
  3a7ef8:	33 d2                	xor    dx,dx
  3a7efa:	bb 0a 00             	mov    bx,0xa
  3a7efd:	f7 f3                	div    bx
  3a7eff:	88 16 a2 ca          	mov    BYTE PTR ds:0xcaa2,dl
  3a7f03:	90                   	nop
  3a7f04:	c3                   	ret
  3a7f05:	90                   	nop
  3a7f06:	b8 01 00             	mov    ax,0x1
  3a7f09:	e7 00                	out    0x0,ax
  3a7f0b:	b8 07 00             	mov    ax,0x7
  3a7f0e:	e8 df 15             	call   0x3a94f0

ROM 3A845A..3A8473

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a845a <.data>:
  3a845a:	01 e8                	add    ax,bp
  3a845c:	44                   	inc    sp
  3a845d:	02 72 06             	add    dh,BYTE PTR [bp+si+0x6]
  3a8460:	e8 bf bf             	call   0x3a4422
  3a8463:	73 eb                	jae    0x3a8450
  3a8465:	90                   	nop
  3a8466:	c3                   	ret
  3a8467:	90                   	nop
  3a8468:	b8 01 00             	mov    ax,0x1
  3a846b:	e7 00                	out    0x0,ax
  3a846d:	b8 08 00             	mov    ax,0x8
  3a8470:	e8 7d 10             	call   0x3a94f0

ROM 3A87C4..3A87DD

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a87c4 <.data>:
  3a87c4:	00 90 e8 17          	add    BYTE PTR [bx+si+0x17e8],dl
  3a87c8:	02 72 05             	add    dh,BYTE PTR [bp+si+0x5]
  3a87cb:	e8 54 bc             	call   0x3a4422
  3a87ce:	73 ee                	jae    0x3a87be
  3a87d0:	c3                   	ret
  3a87d1:	90                   	nop
  3a87d2:	b8 01 00             	mov    ax,0x1
  3a87d5:	e7 00                	out    0x0,ax
  3a87d7:	b8 09 00             	mov    ax,0x9
  3a87da:	e8 13 0d             	call   0x3a94f0

ROM 3A8A48..3A8A61

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a8a48 <.data>:
  3a8a48:	01 e8                	add    ax,bp
  3a8a4a:	a6                   	cmps   BYTE PTR ds:[si],BYTE PTR es:[di]
  3a8a4b:	01 72 06             	add    WORD PTR [bp+si+0x6],si
  3a8a4e:	e8 d1 b9             	call   0x3a4422
  3a8a51:	73 eb                	jae    0x3a8a3e
  3a8a53:	90                   	nop
  3a8a54:	c3                   	ret
  3a8a55:	90                   	nop
  3a8a56:	b8 01 00             	mov    ax,0x1
  3a8a59:	e7 00                	out    0x0,ax
  3a8a5b:	b8 0a 00             	mov    ax,0xa
  3a8a5e:	e8 8f 0a             	call   0x3a94f0

ROM 3A8CF8..3A8D11

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a8cf8 <.data>:
  3a8cf8:	02 e8                	add    ch,al
  3a8cfa:	20 02                	and    BYTE PTR [bp+si],al
  3a8cfc:	72 06                	jb     0x3a8d04
  3a8cfe:	e8 21 b7             	call   0x3a4422
  3a8d01:	73 eb                	jae    0x3a8cee
  3a8d03:	90                   	nop
  3a8d04:	c3                   	ret
  3a8d05:	90                   	nop
  3a8d06:	b8 01 00             	mov    ax,0x1
  3a8d09:	e7 00                	out    0x0,ax
  3a8d0b:	b8 0b 00             	mov    ax,0xb
  3a8d0e:	e8 df 07             	call   0x3a94f0

ROM 3A8F8A..3A8FA3

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a8f8a <.data>:
  3a8f8a:	ce                   	into
  3a8f8b:	02 e8                	add    ch,al
  3a8f8d:	31 02                	xor    WORD PTR [bp+si],ax
  3a8f8f:	72 05                	jb     0x3a8f96
  3a8f91:	e8 8e b4             	call   0x3a4422
  3a8f94:	73 e8                	jae    0x3a8f7e
  3a8f96:	c3                   	ret
  3a8f97:	90                   	nop
  3a8f98:	b8 01 00             	mov    ax,0x1
  3a8f9b:	e7 00                	out    0x0,ax
  3a8f9d:	b8 0c 00             	mov    ax,0xc
  3a8fa0:	e8 4d 05             	call   0x3a94f0

ROM 3A93A6..3A93BF

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003a93a6 <.data>:
  3a93a6:	00 e8                	add    al,ch
  3a93a8:	76 00                	jbe    0x3a93aa
  3a93aa:	72 06                	jb     0x3a93b2
  3a93ac:	e8 73 b0             	call   0x3a4422
  3a93af:	73 eb                	jae    0x3a939c
  3a93b1:	90                   	nop
  3a93b2:	c3                   	ret
  3a93b3:	90                   	nop
  3a93b4:	b8 01 00             	mov    ax,0x1
  3a93b7:	e7 00                	out    0x0,ax
  3a93b9:	b8 0d 00             	mov    ax,0xd
  3a93bc:	e8 31 01             	call   0x3a94f0

ROM 3AA0D4..3AA0ED

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003aa0d4 <.data>:
  3aa0d4:	30 b9 01 00          	xor    BYTE PTR [bx+di+0x1],bh
  3aa0d8:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa0dd:	c3                   	ret
  3aa0de:	1c 84                	sbb    al,0x84
  3aa0e0:	00 20                	add    BYTE PTR [bx+si],ah
  3aa0e2:	b8 01 00             	mov    ax,0x1
  3aa0e5:	e7 00                	out    0x0,ax
  3aa0e7:	b8 0f 00             	mov    ax,0xf
  3aa0ea:	e8 03 f4             	call   0x3a94f0

ROM 3AA664..3AA67D

/workspace/scratch/e06e74fabeed/audit/f37_astra/fragment.bin:     file format binary


Disassembly of section .data:

003aa664 <.data>:
  3aa664:	30 b9 01 00          	xor    BYTE PTR [bx+di+0x1],bh
  3aa668:	9a 4c 25 00 a0       	call   0xa000:0x254c
  3aa66d:	c3                   	ret
  3aa66e:	1c 84                	sbb    al,0x84
  3aa670:	00 20                	add    BYTE PTR [bx+si],ah
  3aa672:	b8 01 00             	mov    ax,0x1
  3aa675:	e7 00                	out    0x0,ax
  3aa677:	b8 10 00             	mov    ax,0x10
  3aa67a:	e8 73 ee             	call   0x3a94f0
