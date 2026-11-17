---
layout: page
permalink: /research/
title: Research
description:
nav: true
nav_order: 2
---

I work at the intersection of condensed matter physics and quantum information. My current research covers:

- [Quantum error correction and fault-tolerant quantum computation](#quantum-error-correction-and-fault-tolerant-quantum-computation)
- [Topological holography](#topological-holography)
- [Generalized symmetries in topological matter and quantum codes](#generalized-symmetries-in-topological-quantum-matter-and-quantum-error-correcting-codes)
- [Crystalline and quasicrystalline topological phases](#crystalline-and-quasicrystalline-topological-phases)
- [Topological invariants for higher-order topological superconductors](#topological-invariants-for-higher-order-topological-superconductors)
- [Fractons](#fractons)

{% comment %}
  To add a figure to a section, put the image in assets/img/research/ and paste this under the heading:
  ![Short description of the figure](/assets/img/research/your-figure.png)
{% endcomment %}

---

#### Quantum error correction and fault-tolerant quantum computation

In fault-tolerant quantum computing with the surface code, non-Clifford gates are essential for achieving universal computation. However, existing approaches, such as magic state distillation and code switching, are resource-intensive. My collaborators and I have proposed a protocol that combines magic state preparation with code switching to implement logical non-Clifford operations.

Our approach starts with a specially prepared logical state in the $$\mathbb{Z}_4$$ surface code. Through a sequence of transformations involving gauging and anyon condensation, the system transitions through various topological codes, notably including the non-Abelian $$D_4$$ quantum double model. This process ultimately produces a magic state in a condensed $$\mathbb{Z}_2$$ surface code, which enables the implementation of a logical T gate in the standard $$\mathbb{Z}_2$$ surface code through gate teleportation.

We have also generalized standard lattice surgery to hybrid lattice surgery, in which rough merge and rough split operations happen across different topological codes. Applying these procedures between Abelian and non-Abelian codes provides non-Clifford operations in the standard surface code, in the form of a magic state or a non-Clifford gate teleportation. We also give a continuum topological field theory description of hybrid lattice surgery using interfaces between (2+1)d topological orders.

**Related publications**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=2610.27556 || arxiv=2510.20890 || arxiv=2502.00998] %}
</div>

#### Topological holography

The essential idea of topological holography is to encode a generalized symmetry and its symmetry charges into a topological order in one higher dimension. This topological order goes by several names, such as symmetry topological field theory (SymTFT) or symmetry topological order (SymTO).

Together with Meng Cheng, I have applied the topological holography picture to a variety of exotic quantum critical points and gapless phases in (1+1)d. These include:

- phase transitions between SPT phases;
- symmetry-enriched quantum critical points (transitions between an SPT and a symmetry-breaking phase);
- deconfined quantum critical points;
- intrinsically gapless SPT phases.

Many of these exotic quantum critical points and gapless phases can be characterized by non-trivial responses in the symmetry defect operators and twisted partition functions. We also developed a topological holographic picture for conformal boundary states of (1+1)d RCFTs, which uncovers the nature of the gapped phases that correspond to those boundary states.

I have further generalized the topological holography picture to fermionic systems and studied exotic fermionic quantum critical points from this viewpoint. More recently, my collaborators and I have extended this picture to (2+1)d gapped and gapless phases with non-invertible symmetries, and developed a general construction of lattice models for (2+1)d gapped phases with non-invertible symmetries.

What I like about this picture is that it lets us use the intuition and techniques of topological order to derive general statements about critical points and gapless phases.

**Related publications**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=2506.09177 || arxiv=2503.12699 || arxiv=2405.09611 || arxiv=2310.16878] %}
</div>

#### Generalized symmetries in topological quantum matter and quantum error-correcting codes

Symmetry has played a crucial role in classifying quantum matter. The notion of global symmetry has recently been generalized in both the condensed matter and high-energy communities to include higher-form, higher-group, and non-invertible symmetries. An emerging picture is that generalized symmetry is equivalent to topological defects, summarized by the slogan "Symmetry = Topological defect".

My colleagues and I have investigated different aspects of topological defects in (3+1)d topological orders. We give several general constructions of codimension-2 defects through (1) gauging lower-dimensional invertible (SPT) phases, (2) layer constructions, and (3) anyon condensation. We also uncover part of the 3-group structure that captures the interplay between codimension-2 defects and defects of lower codimension.

The mathematical description of this 3-group structure translates into transversal logical gates in the corresponding topological error-correcting codes: it corresponds to non-trivial commutation relations between logical gates that fit into the Clifford hierarchy. This connection reveals the essential role of higher-group structure in the existence of transversal non-Clifford gates.

**Related publication**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=2208.07367] %}
</div>

#### Crystalline and quasicrystalline topological phases

Crystalline symmetry can protect non-trivial topological phases and leads to interesting higher-order boundary phenomena such as hinge or corner modes. I have developed a general theoretical framework, the topological crystal approach, to systematically classify and characterize these phases. The essential idea is that any topological crystalline phase has a corresponding real-space crystalline stacking pattern of lower-dimensional topological states, which we systematically classified.

I have applied this approach to classify bosonic crystalline SPT phases and fermionic topological crystalline insulators (TCIs). Based on this picture, I have also studied surface field theories for bosonic SPT phases with point group symmetry, as well as exotic crystalline SPT phases and their surface theories in 4d space. More recently, I have generalized the topological crystal approach to classify interacting Dirac semimetals. The framework has a clear physical picture, applies to both bosonic and fermionic systems, readily incorporates strong interactions, and gives access to boundary signatures and topological responses.

Given this progress in classifying crystalline topological phases, a natural question is whether topological phenomena can be protected by the structure of quasicrystals. Building on the topological crystal framework, my collaborators and I have studied quasicrystalline topological phases and their topological responses. We also found intrinsically quasicrystalline phases, which have no crystalline analogs.

**Related publications**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=2211.03802 || arxiv=2107.03409 || arxiv=2103.13393 || arxiv=2001.07772 || arxiv=1811.06558 || arxiv=1810.02330 || arxiv=1711.03649 || arxiv=1705.09243 || arxiv=1604.08151] %}
</div>

#### Topological invariants for higher-order topological superconductors

In searching for material realizations of crystalline topological phases with non-trivial band topology, identifying topological invariants in momentum space is the primary task, but deriving them from formal classification results is difficult. Topological superconductors are exotic topological quantum matter that supports Majorana boundary modes, which have attracted extensive theoretical and experimental attention because of their potential application to quantum computation. Under the protection of crystalline symmetries, 2D and 3D superconductors can host Majorana corner or hinge modes.

My collaborators and I have proposed a general procedure to derive topological invariants: symmetry indicators, which are defined at high-symmetry momenta, and also invariants beyond symmetry indicators. Our approach establishes a bulk-boundary correspondence using the classification in both real and momentum space. From these invariants, we derived general recipes that can guide material searches and design for higher-order topological superconductors.

**Related publications**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=2212.06197 || arxiv=2109.06959 || arxiv=2010.05947] %}
</div>

#### Fractons

Non-Abelian quasiparticles are fascinating excitations of quantum many-body systems: they spread quantum information nonlocally and have exotic braiding properties. While non-Abelian quasiparticles occur in theoretical models in two spatial dimensions, one factor limiting their realization in 3D is that fully mobile quasiparticles in 3D can only be bosons or fermions. We showed that this limitation is circumvented in so-called fracton phases of matter.

We introduced a class of gapped 3D fracton models, dubbed "cage-net fracton models", which host immobile fracton excitations in addition to non-Abelian particles with restricted mobility. Starting from layers of two-dimensional string-net models, whose spectrum includes non-Abelian anyons, we condense extended one-dimensional "flux strings" built out of pointlike excitations. Flux-string condensation generalizes anyon condensation from conventional topological order and lets us establish properties of the fracton-ordered phase, such as its ground-state wave function and spectrum of excitations. The ground state of such phases can be understood as a fluctuating network of extended objects (cages and strings), which we call a cage-net condensate.

A second class of models we introduced can be viewed as gauging certain subsystem symmetries in the $$d = 3$$ Abelian Dijkgraaf-Witten models. These models can support non-Abelian fractons for certain choices of non-Abelian gauge groups. I have also used quantum information tools such as entanglement entropy and entanglement spectra to characterize fracton orders and subsystem SPT phases.

**Related publications**

<div class="publications">
{% bibliography --group_by none --query @*[arxiv=1901.10486 || arxiv=1806.04687 || arxiv=1805.06899] %}
</div>
