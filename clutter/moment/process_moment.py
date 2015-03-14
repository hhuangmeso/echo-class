#!/usr/bin/python

import os
import json
import getpass
import argparse
import numpy as np

from pyart.config import get_field_name

from clutter.moment import moment_fields

### GLOBAL VARIABLES ###
########################

# Define basic values and thresholds
MIN_NCP = 0.3
VCP_SWEEPS = 22
VCP_RAYS = None
MIN_SWEEP = None
MAX_SWEEP = 0

# Define bins and limits for moment histograms
BINS_REFL, LIMITS_REFL = 200, (-40.0, 50.0)
BINS_VDOP, LIMITS_VDOP = 200, (-20.0, 20.0)
BINS_SW, LIMITS_SW = 100, (0, 10)
BINS_RHOHV, LIMITS_RHOHV = 50, (0, 1)
BINS_ZDR, LIMITS_ZDR = 250, (-20, 30)
BINS_NCP, LIMITS_NCP = 100, (0, 1)

# Define fields to exclude from radar object
EXCLUDE_FIELDS = [
    'radar_echo_classification',
    'corrected_reflectivity',
    'differential_phase',
    ]

# Parse field names
refl_field = get_field_name('reflectivity')
vdop_field = get_field_name('velocity')
sw_field = get_field_name('spectrum_width')
rhohv_field = get_field_name('cross_correlation_ratio')
zdr_field = get_field_name('differential_reflectivity')
ncp_field = get_field_name('normalized_coherent_power')
phidp_field = get_field_name('differential_phase')


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('json', type=str, help=None)
    parser.add_argument('pickle', type=str, help=None)
    parser.add_argument('--inpdir', nargs='?', type=str, const='', default='',
                        help=None)
    parser.add_argument('--outdir', nargs='?', type=str, const='', default='',
                        help=None)
    parser.add_argument('-v', '--verbose', nargs='?', type=bool, const=True,
                        default=False, help=None)
    parser.add_argument('-db', '--debug', nargs='?', type=bool, const=True,
                        default=False, help=None)
    args = parser.parse_args()

    if args.debug:
        print 'json = %s' % args.json
        print 'pickle = %s' % args.pickle
        print 'inpdir = %s' % args.inpdir
        print 'outdir = %s' % args.outdir

    if args.verbose:
        print 'MIN_NCP = %.2f' % MIN_NCP
        print 'VCP_SWEEPS = %s' % VCP_SWEEPS
        print 'VCP_RAYS = %s' % VCP_RAYS
        print 'MIN_SWEEP = %s' % MIN_SWEEP
        print 'MAX_SWEEP = %s' % MAX_SWEEP

    # Compute histograms for specified moments
    if args.verbose:
        print 'Processing reflectivity'
    refl = moment_fields.histogram_from_json(
        args.json, refl_field, inpdir=args.inpdir, bins=BINS_REFL,
        limits=LIMITS_REFL, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    if args.verbose:
        print 'Processing Doppler velocity'
    vdop = moment_fields.histogram_from_json(
        args.json, vdop_field, inpdir=args.inpdir, bins=BINS_VDOP,
        limits=LIMITS_VDOP, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    if args.verbose:
        print 'Processing spectrum width'
    sw = moment_fields.histogram_from_json(
        args.json, sw_field, inpdir=args.inpdir, bins=BINS_SW,
        limits=LIMITS_SW, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    if args.verbose:
        print 'Processing copolar correlation'
    rhohv = moment_fields.histogram_from_json(
        args.json, rhohv_field, inpdir=args.inpdir, bins=BINS_RHOHV,
        limits=LIMITS_RHOHV, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    if args.verbose:
        print 'Processing differential reflectivity'
    zdr = moment_fields.histogram_from_json(
        args.json, zdr_field, inpdir=args.inpdir, bins=BINS_ZDR,
        limits=LIMITS_ZDR, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    if args.verbose:
        print 'Processing normalized coherent power'
    ncp = moment_fields.histogram_from_json(
        args.json, ncp_field, inpdir=args.inpdir, bins=BINS_NCP,
        limits=LIMITS_NCP, min_ncp=MIN_NCP, vcp_sweeps=VCP_SWEEPS,
        vcp_rays=VCP_RAYS, min_sweep=MIN_SWEEP, max_sweep=MAX_SWEEP,
        exclude_fields=EXCLUDE_FIELDS, fill_value=None, ncp_field=ncp_field,
        verbose=args.verbose)

    # Pack histograms together
    histograms = [refl, vdop, sw, rhohv, zdr, ncp]

    # Pickle moment histograms
    moment_fields._pickle_histograms(
        histograms, args.pickle, outdir=args.outdir)
