# -*- coding: utf-8 -*-
"""
Structural analysis for plane trusses.

@author: Nicolás Guarín-Zapata
@date: March 2023
"""
from datetime import datetime
import numpy as np


def analysis(data, verbose=False):
    """
    Run a complete workflow for the analysis of a plane truss structure

    Parameters
    ----------
    data : dict
        Simulation data composed of nodes, constrains, elements,
        materials and loads.
    verbose : bool
        Flag to print messages related to the analysis.

    Returns
    -------
    displ : ndarray (nnodes, 2)
        Displacements at nodes.

    """
    # Retrieving data
    nodes = data["nodes"]
    cons = data["cons"]
    elements = data["elements"]
    mats = data["mats"]
    loads = data["loads"]

    # Pre-processing
    assem_op, bc_array, neq = node2dof(cons, elements)
    if verbose:
      print("Number of nodes: {}".format(nodes.shape[0]))
      print("Number of elements: {}".format(elements.shape[0]))
      print("Number of equations: {}".format(neq))

    # System assembly
    stiff_mat = assem(elements, mats, nodes, neq, assem_op)
    rhs_vec = loadasem(loads, bc_array, neq)

    # System solution
    start_time = datetime.now()
    disp = np.linalg.solve(stiff_mat, rhs_vec)


    if verbose:
      if not np.allclose(stiff_mat.dot(disp)/stiff_mat.max(),
                         rhs_vec/stiff_mat.max()):
          print("The system is not in equilibrium!")
    end_time = datetime.now()
    if verbose:
      print('Duration for system solution: {}'.format(end_time - start_time))

    # Post-processing
    disp_complete = complete_disp(bc_array, nodes, disp)
    return disp_complete


#%% Assembly
def eqcounter(cons):
    """Count active equations

    Creates boundary conditions array bc_array

    Parameters
    ----------
    cons : ndarray.
      Array with constraints for each node.

    Returns
    -------
    neq : int
      Number of equations in the system after removing the nodes
      with imposed displacements.
    bc_array : ndarray (int)
      Array that maps the nodes with number of equations.

    """
    nnodes = cons.shape[0]
    bc_array = cons.copy()
    neq = 0
    for i in range(nnodes):
        for j in range(2):
            if bc_array[i, j] == 0:
                bc_array[i, j] = neq
                neq += 1

    return neq, bc_array


def node2dof(cons, elements):
    """Create node-to-dof map

    Count active equations, create boundary conditions array ``bc_array``
    and the assembly operator ``assem_op``.

    Parameters
    ----------
    cons : ndarray.
      Array with constraints for each degree of freedom in each node.
    elements : ndarray
      Array with the number for the nodes in each element.

    Returns
    -------
    assem_op : ndarray (int)
      Assembly operator.
    bc_array : ndarray (int)
      Boundary conditions array.
    neq : int
      Number of active equations in the system.

    """
    nels = elements.shape[0]
    assem_op = np.zeros([nels, 4], dtype=int)
    neq, bc_array = eqcounter(cons)
    for ele in range(nels):
        assem_op[ele, :] = bc_array[elements[ele, 1:], :].flatten()
    return assem_op, bc_array, neq


def assem(elements, mats, nodes, neq, assem_op):
    """
    Assembles the global stiffness matrix
    using a dense storing scheme

    Parameters
    ----------
    elements : ndarray (int)
      Array with the number for the nodes in each element.
    mats : ndarray (float)
      Array with the material profiles.
    nodes : ndarray (float)
      Array with the nodal numbers and coordinates.
    assem_op : ndarray (int)
      Assembly operator.
    neq : int
      Number of active equations in the system.
    uel : callable function (optional)
      Python function that returns the local stiffness matrix.

    Returns
    -------
    kglob : ndarray (float)
      Array with the global stiffness matrix in a dense numpy
      array.

    """
    kglob = np.zeros((neq, neq))
    nels = elements.shape[0]
    for ele in range(nels):
        params = mats[elements[ele, 0], :]
        elcoor = nodes[elements[ele, 1:], :]
        kloc = truss2D(elcoor, params)
        dme = assem_op[ele, :]
        for row in range(4):
            glob_row = dme[row]
            if glob_row != -1:
                for col in range(4):
                    glob_col = dme[col]
                    if glob_col != -1:
                        kglob[glob_row, glob_col] += kloc[row, col]

    return kglob


def loadasem(loads, bc_array, neq):
    """Assembles the global Right Hand Side Vector

    Parameters
    ----------
    loads : ndarray
      Array with the loads imposed in the system.
    bc_array : ndarray (int)
      Array that maps the nodes with number of equations.
    neq : int
      Number of equations in the system after removing the nodes
      with imposed displacements.

    Returns
    -------
    rhs_vec : ndarray
      Array with the right hand side vector.

    """
    nloads = loads.shape[0]
    rhs_vec = np.zeros([neq])
    for cont in range(nloads):
        for dof in range(2):
            dof_id = bc_array[cont, dof]
            if dof_id != -1:
                rhs_vec[dof_id] = loads[cont, dof]
    return rhs_vec


#%% Elements
def truss2D(coord, params):
    """2D 2-noded truss element

    Parameters
    ----------
    coord : ndarray
      Coordinates for the nodes of the element (2, 2).
    params : tuple
      Element parameters in the following order:

          young : float
            Young modulus (>0).
          area : float
            Cross-sectional area (>0).

    Returns
    -------
    stiff_mat : ndarray
      Local stiffness matrix for the element (4, 4).

    Examples
    --------

    >>> coord = np.array([
    ...         [0, 0],
    ...         [1, 0]])
    >>> params = [1.0 , 1.0]
    >>> stiff = truss2D(coord, params)
    >>> stiff_ex =  np.array([
    ...    [1, 0, -1, 0],
    ...    [0, 0, 0, 0],
    ...    [-1, 0, 1, 0],
    ...    [0, 0, 0, 0]])
    >>> np.allclose(stiff, stiff_ex)
    True

    """
    vec = coord[1, :] - coord[0, :]
    length = np.linalg.norm(vec)
    nx = vec[0]/length
    ny = vec[1]/length
    Q = np.array([
        [nx, ny, 0, 0],
        [0, 0, nx, ny]])
    young, area  = params
    stiff = area*young/length
    stiff_mat = stiff * np.array([
        [1, -1],
        [-1, 1]])
    stiff_mat = Q.T @ stiff_mat @ Q
    return stiff_mat


#%% Postprocessing
def complete_disp(bc_array, nodes, sol):
    """
    Fill the displacement vectors with imposed and computed values.

    bc_array : ndarray (int)
        Indicates if the nodes has any type of boundary conditions
        applied to it.
    sol : ndarray (float)
        Array with the computed displacements.
    nodes : ndarray (float)
        Array with number and nodes coordinates

    Returns
    -------
    sol_complete : (nnodes, 2) ndarray (float)
      Array with the displacements.

    """
    nnodes = nodes.shape[0]
    sol_complete = np.zeros([nnodes, 2], dtype=float)
    for row in range(nnodes):
        for col in range(2):
            cons = bc_array[row, col]
            if cons == -1:
                sol_complete[row, col] = 0.0
            else:
                sol_complete[row, col] = sol[cons]
    return sol_complete


if __name__ == "__main__":
    nodes = np.array([
        [8.66, 0.0],
        [0.0, 5.0],
        [0.0, 0.0]])
    cons = np.array([
        [0, 0],
        [-1, 0],
        [-1, -1]], dtype=int)
    elements = np.array([
        [0, 2, 0],
        [0, 0, 1],
        [0, 1, 2]], dtype=int)
    loads = np.array([
        [0.0, -10.0],
        [0.0, 0.0],
        [0.0, 0.0]])
    mats = np.array([
        [1e3, 0.1]])

    data = {
      "nodes": nodes,
      "cons": cons,
      "elements": elements,
      "loads": loads,
      "mats": mats}
    disp = analysis(data, verbose=True)
