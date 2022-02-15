import { HttpErrorResponse, HttpHeaderResponse, HttpHeaders } from '@angular/common/http';
import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Table } from 'primeng/table';
import { Areas } from 'src/app/models/area.model';
import { OfficialDocument } from 'src/app/models/official-documents.model';
import { AreasService } from 'src/app/services/areas.service';
import { OfficialDocumentsService } from 'src/app/services/official-documents.service';
import Swal from 'sweetalert2';

declare let jsPDF;

@Component({
  selector: 'app-official-documents',
  templateUrl: './official-documents.component.html',
  styleUrls: [
    './official-documents.component.css',
  ]
})
export class OfficialDocumentsComponent {

  @ViewChild('modal_delete', { static: true }) modal_delete: ElementRef<any>;
  @ViewChild('modal_update', { static: true }) modal_update: ElementRef<any>;
  @ViewChild('modal_create', { static: true }) modal_create: ElementRef<any>;
  @ViewChild('dt1') dt: Table

  //PrimeNG variables
  public table_cols = [
    { field: 'name', header: 'Documento Oficial' },
    { field: 'classification_name', header: 'Clasificación' },
    { field: 'link', header: 'Vínculo de acceso' },
    { field: 'area_name', header: 'Área' },
    { field: 'actions', header: 'Acciones' },
  ];
  public _selected_columns: any = [];
  public export_columns: any = [];
  public lazy = false;

  //new
  public documents: Array<OfficialDocument>;
  public areas: Array<Areas>;
  public classifications: any;
  public selected_document: OfficialDocument;
  public file_to_upload: File | null = null;
  public file_error: string = null;
  public current_index: number;
  public document_form = this.fb.group({
    name: [null, Validators.required],
    classification: ['', Validators.required],
    area: ['', Validators.required]
  });

  constructor(
    private modal_service: NgbModal,
    private documents_service: OfficialDocumentsService,
    private area_service: AreasService,
    private fb: FormBuilder,
  ) {
  }

  ngOnInit(): void {
    this._selected_columns = this.table_cols;
    this.export_columns = this.table_cols.map(col => ({ title: col.header, dataKey: col.field }));
    //new
    this.documents_service.list().subscribe((resp: Array<OfficialDocument>) => {
      this.documents = resp;
    }, (error: HttpErrorResponse) => {
      console.log(error);
      Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
    })
    this.documents_service.get_classifications().subscribe((resp: any) => {
      this.classifications = resp;
    }, (error: HttpErrorResponse) => {
      console.log(error);
      Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
    });
    this.area_service.list().subscribe((resp: Array<Areas>) => {
      this.areas = resp;
    }, (error: HttpErrorResponse) => {
      console.log(error);
      Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
    });
  }

  validate_control(value: string) {
    if (this.document_form.controls[value].pristine && this.document_form.controls[value].errors == null)
      return 'form-control';
    if (this.document_form.controls[value].touched && this.document_form.controls[value].errors?.required)
      return 'form-control is-invalid'
    else
      return 'form-control'
  }

  close_modal() {
    this.document_form.reset();
    this.document_form.patchValue({ name: '' });
    this.document_form.patchValue({ area: '' });
    this.document_form.patchValue({ classification: '' });
    this.document_form.removeControl('file')
    this.document_form.removeControl('link');
    this.file_to_upload = null;
    this.file_error = null;
    this.selected_document = null;
    this.current_index = null;
    this.modal_service.dismissAll();
  }

  open_modal_update(index) {
    this.selected_document = this.documents[index];
    this.current_index = index;
    this.document_form.patchValue({ name: this.selected_document.name })
    this.document_form.patchValue({ area: this.selected_document.area })
    this.document_form.patchValue({ classification: this.selected_document.classification })
    if (this.selected_document.link != '')
      this.document_form.addControl('link', new FormControl(this.selected_document.link, Validators.required));
    this.modal_service.open(this.modal_update, { centered: true, backdrop: 'static' })
  }

  confirm_update() {
    if (this.document_form.valid) {
      let form_data: FormData = new FormData();
      let changes = false;
      Object.keys(this.document_form.controls).forEach(key => {
        if (!this.document_form.get(key).pristine && (this.document_form.get(key).touched || this.document_form.get(key).dirty)) {
          changes = true;
          if (key == 'file')
            form_data.append('file', this.file_to_upload, this.file_to_upload.name);
          else
            form_data.append(key, this.document_form.get(key).value);
        }
      });
      if (changes) {
        this.documents_service.update(this.selected_document.id, form_data).subscribe((resp: OfficialDocument) => {
          this.documents_service.list().subscribe((resp: Array<OfficialDocument>) => {
            this.documents = resp;
            this.close_modal();
            Swal.fire('¡Transacción exitosa!', 'El Documento Oficial ha sido actualizado.', 'success');
          }, (error: HttpErrorResponse) => {
            console.log(error);
            Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
          })
        }, (error: HttpErrorResponse) => {
          console.log(error);
          if (error.status == 400) {
            Object.keys(error.error).forEach(key => {
              switch (key) {
                case 'name':
                  this.document_form.get('name').setErrors({ 'name_error': true, message: error.error.name });
                  break;
                case 'classification':
                  this.document_form.get('classification').setErrors({ 'classification_error': true, message: error.error.classification });
                  break;
                case 'link':
                  this.document_form.get('link').setErrors({ 'link_error': true, message: error.error.link });
                  break;
                case 'file':
                  this.document_form.get('file').setErrors({ 'file_error': true, message: error.error.file });
                  break;
                case 'area':
                  this.document_form.get('area').setErrors({ 'area_error': true, message: error.error.area });
                  break;
              }
            })
          }
          else {
            Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
          }
        })
      }
      else
        Swal.fire('¡Error!', 'No se ha realizado ninguna modificación.', 'error');
    }
  }

  open_modal_delete(index: number) {
    this.selected_document = this.documents[index];
    let title: string;
    let message: string;
    if (this.selected_document.deleted == null) {
      title = '¿Está seguro que desea desactivar este registro?';
      message = 'El Documento Oficial ha sido desactivado';
    }
    else {
      title = '¿Está seguro que desea activar este registro?';
      message = 'El Documento Oficial ha sido activado';
    }
    Swal.fire({
      title: title,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: 'green',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Confirmar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.documents_service.delete(this.selected_document.id).subscribe((resp: any) => {
          this.documents_service.list().subscribe((resp: Array<OfficialDocument>) => {
            this.documents = resp;
            Swal.fire('¡Transacción exitosa!', message, 'success');
          }, (error: HttpErrorResponse) => {
            console.log(error);
            Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
          });
        }, (error: HttpErrorResponse) => {
          console.log(error);
          Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
        });
      }
    })
  }

  open_modal_create() {
    this.document_form.addControl('file', new FormControl('', Validators.required));
    this.document_form.addControl('link', new FormControl('', Validators.required));
    this.modal_service.open(this.modal_create, { centered: true, backdrop: 'static' });
  }

  confirm_create() {
    console.log(this.document_form);
    if (this.document_form.valid) {
      let form_data: FormData = new FormData();
      Object.keys(this.document_form.controls).forEach(key => {
        if (key == 'file') {
          form_data.append('file', this.file_to_upload, this.file_to_upload.name);
        }
        else {
          form_data.append(key, this.document_form.get(key).value);
        }
      });
      this.documents_service.create(form_data).subscribe((resp: OfficialDocument) => {
        this.documents_service.list().subscribe((resp: Array<OfficialDocument>) => {
          this.documents = resp;
          Swal.fire('¡Transacción exitosa!', 'El Documento Oficial ha sido creado', 'success');
          this.close_modal();
        }, (error: HttpErrorResponse) => {
          console.log(error);
        });
      }, (error: HttpErrorResponse) => {
        console.log(error);
        if (error.status == 400) {
          Object.keys(error.error).forEach(key => {
            switch (key) {
              case 'name':
                this.document_form.get('name').setErrors({ 'name_error': true, message: error.error.name });
                break;
              case 'classification':
                this.document_form.get('classification').setErrors({ 'classification_error': true, message: error.error.classification });
                break;
              case 'link':
                this.document_form.get('link').setErrors({ 'link_error': true, message: error.error.link });
                break;
              case 'file':
                this.document_form.get('file').setErrors({ 'file_error': true, message: error.error.file });
                break;
              case 'area':
                this.document_form.get('area').setErrors({ 'area_error': true, message: error.error.area });
                break;
            }
          })
        }
        else {
          Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
        }
      })

    }
  }

  check_control_exists(name: string, condition: boolean) {
    const control = this.document_form.get(name);
    if (!control && condition) {
      this.document_form.addControl(name, new FormControl('', Validators.required));
    }
    if (control && !condition) {
      this.document_form.removeControl(name);
    }
  }

  //Manejo de archivos
  handle_file_input(files: any) {
    console.log(this.document_form);
    let file = files.target.files.item(0)
    if (file.type != 'application/pdf') {
      this.file_to_upload = null;
      this.file_error = 'Solo se aceptan archivos en formato PDF.'
    }
    else {
      this.file_to_upload = file;
      this.file_error = null;
      if (!this.document_form.get('file')) {
        this.document_form.addControl('file', new FormControl(null, Validators.required));
      }
      this.document_form.get('file').markAsDirty();
      this.document_form.patchValue({ file: this.file_to_upload });
      console.log(this.document_form);
    }
  }

  download_file(document_to_dowload:OfficialDocument) {
    if(document_to_dowload.has_file){
      this.documents_service.download(document_to_dowload.id).subscribe((resp: any) => {
        console.log(resp);      
        let data = resp.body;
        let data_type = data.type;
        let binaryData = [];
        binaryData.push(data);
        let download_link = document.createElement('a');
        download_link.href = window.URL.createObjectURL(new Blob(binaryData, { type: data_type }));
        let filename = '';
        let disposition = resp.headers.get('content-disposition')
        if (disposition && disposition.indexOf('inline') !== -1) {
          var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          var matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, '');
          }
        }
        console.log(filename);
        if (filename)
            download_link.setAttribute('download', filename);
        document.body.appendChild(download_link);
        download_link.click(); 
        download_link.parentNode.removeChild(download_link);
      },(error:HttpErrorResponse)=>{
        console.log(error);      
        Swal.fire('¡Error!', 'Se produjo un error inesperado en el servidor', 'error');
      });
    }
  }

  file_radio_change(radio: any) {
    let value = radio.target.value;
    switch (value) {
      case 'link':
        this.check_control_exists('link', true);
        this.check_control_exists('file', false);
        break;
      case 'file':
        this.check_control_exists('file', true);
        this.check_control_exists('link', false);
        break;
      case 'both':
        this.check_control_exists('file', true);
        this.check_control_exists('link', true);
        break;
    }
  }

  set_update_radio(option: string) {
    switch (option) {
      case 'file':
        return this.document_form.get(option);
      case 'link':
        return this.document_form.get(option);
      case 'both':
        return (this.document_form.get('file') && this.document_form.get('link'))
      case 'neither':
        return (!this.document_form.get('file') && !this.document_form.get('link'))
    }
    return false;
  }

  find_index(obj) {
    let index;
    this.documents.find((item, i) => {
      if (item.id == obj.id)
        index = i;
    })
    return index;
  }

  set_delete_image_class(data: any) {
    let document = this.documents[this.find_index(data)];
    if (document.deleted == null)
      return 'fas fa-toggle-on';
    else
      return 'fas fa-toggle-off';
  }

  set_delete_button_class(data: any) {
    let document = this.documents[this.find_index(data)];
    if (document.deleted == null)
      return 'btn btn-success rounded-circle';
    else
      return 'btn btn-danger rounded-circle';
  }

  //PrimeNG Functions and Procedures
  apply_filter($event, stringVal) {
    this.dt?.filterGlobal(($event.target as HTMLInputElement).value, 'contains');
  }

  clear(table: Table) {
    table.clear();
  }

  @Input() get selected_columns(): any[] {
    return this._selected_columns;
  }

  set selected_columns(val: any[]) {
    //restore original order
    this._selected_columns = this.table_cols.filter(col => val.includes(col));
  }

  export_pdf() {
    import("jspdf-autotable").then(x => {
      let doc = new jsPDF('p', 'pt');
      doc.autoTable(this.export_columns, this.documents);
      doc.save('products.pdf');
    })
  }

  export_excel() {
    import("xlsx").then(xlsx => {
      const worksheet = xlsx.utils.json_to_sheet(this.documents);
      const workbook = { Sheets: { 'data': worksheet }, SheetNames: ['data'] };
      const excelBuffer: any = xlsx.write(workbook, { bookType: 'xlsx', type: 'array' });
      this.save_as_excel(excelBuffer, "documents");
    });
  }

  save_as_excel(buffer: any, fileName: string): void {
    import("file-saver").then(FileSaver => {
      let EXCEL_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
      let EXCEL_EXTENSION = '.xlsx';
      const data: Blob = new Blob([buffer], {
        type: EXCEL_TYPE
      });
      FileSaver.saveAs(data, fileName + '_export_' + new Date().getTime() + EXCEL_EXTENSION);
    });
  }

}
