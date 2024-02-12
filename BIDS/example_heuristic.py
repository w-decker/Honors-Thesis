import os


def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    t1w = create_key("sub-{subject}/anat/sub-{subject}_T1w")
    rest = create_key("sub-{subject}/func/sub-{subject}_task-rest_bold")
    dwi = create_key("sub-{subject}/dti/sub-{subject}_dti")
    stat_learning = create_key("sub-{subject}/func/sub-{subject}_task-statlearning_bold")

    info = {t1w: [], rest: [], dwi: [], stat_learning: []}

    for s in seqinfo:
        if "SAG_MPRAGE" in s.series_description:
            info[t1w].append(s.series_id)

        if "DTI" in s.series_description:
            info[dwi].append(s.series_id)

        if "Resting fMRI" in s.series_description:
            info[rest].append({'item': s.series_id})

        if "Learning fMRI" in s.series_description:
            info[stat_learning].append({'item': s.series_id})

    return info
